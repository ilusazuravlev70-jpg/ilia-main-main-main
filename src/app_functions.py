import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "db" / "shoe_store.sqlite"

# --- БЛОК 1. Функции для обработки данных ---

def calc_discount(price, discount_percent):
    if price is None or discount_percent is None:
        return 0.0
    if discount_percent < 0: discount_percent = 0
    if discount_percent > 100: discount_percent = 100
    return round(price - (price * discount_percent / 100), 2)

def pluralize_items(count):
    if count is None: return "0 товаров"
    count = abs(int(count))
    if 11 <= (count % 100) <= 14:
        return f"{count} товаров"
    last_digit = count % 10
    if last_digit == 1:
        return f"{count} товар"
    elif 2 <= last_digit <= 4:
        return f"{count} товара"
    else:
        return f"{count} товаров"

def format_full_name(last, first, middle):
    if not last or not first:
        return "Аноним"
    
    def capitalize_safe(s):
        return s.strip().title() if s else ""
        
    last = capitalize_safe(last)
    first = capitalize_safe(first)
    middle = capitalize_safe(middle)
    
    if middle:
        return f"{last} {first[0]}.{middle[0]}."
    else:
        return f"{last} {first[0]}."

def get_client_tier(total_spent):
    if total_spent is None or total_spent < 0:
        return "Без статуса"
    if total_spent < 5000: return "Новичок"
    if total_spent < 20000: return "Бронза"
    if total_spent < 50000: return "Серебро"
    if total_spent < 100000: return "Золото"
    return "Платина"

def get_client_loyalty_days(first_order_date_str):
    if not first_order_date_str:
        return 0
    try:
        first_date = datetime.strptime(first_order_date_str, "%Y-%m-%d")
        delta = datetime.now() - first_date
        return delta.days
    except ValueError:
        return 0

# --- БЛОК 2. Эмуляция процедур (Транзакции) ---

def place_order(conn, user_id, product_id, size_id, quantity):
    try:
        cur = conn.cursor()
        
        # Проверка пользователя
        cur.execute("SELECT 1 FROM users WHERE user_id = ?", (user_id,))
        if not cur.fetchone():
            return False
            
        # Поиск позиции на складе
        cur.execute("SELECT stock_item_id, price FROM stock_items WHERE product_id = ? AND size_id = ?", (product_id, size_id))
        stock_row = cur.fetchone()
        if not stock_row or stock_row[1] is None:
            return False
            
        stock_item_id, price = stock_row
        
        # Проверка остатка
        cur.execute("SELECT quantity_available FROM stock_items WHERE stock_item_id = ?", (stock_item_id,))
        available = cur.fetchone()[0]
        if available < quantity:
            return False
            
        # Начало транзакции (в sqlite3 она начинается автоматически при первом изменении)
        
        # Создание заказа
        cur.execute("INSERT INTO orders (order_date, user_id) VALUES (?, ?)", (datetime.now().strftime("%Y-%m-%d"), user_id))
        order_id = cur.lastrowid
        
        # Создание позиции заказа
        cur.execute("INSERT INTO order_items (order_id, stock_item_id, quantity, price) VALUES (?, ?, ?, ?)", 
                    (order_id, stock_item_id, quantity, price))
        
        # Списание остатка
        cur.execute("UPDATE stock_items SET quantity_available = quantity_available - ? WHERE stock_item_id = ?", 
                    (quantity, stock_item_id))
                    
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"Ошибка в place_order: {e}")
        return False

def cancel_order(conn, order_id):
    try:
        cur = conn.cursor()
        
        # Проверка заказа
        cur.execute("SELECT 1 FROM orders WHERE order_id = ?", (order_id,))
        if not cur.fetchone():
            return False
            
        # Получение позиций заказа
        cur.execute("SELECT stock_item_id, quantity FROM order_items WHERE order_id = ?", (order_id,))
        items = cur.fetchall()
        
        # Возврат остатков на склад
        for item in items:
            cur.execute("UPDATE stock_items SET quantity_available = quantity_available + ? WHERE stock_item_id = ?", 
                        (item[1], item[0]))
                        
        # Удаление позиций и заказа
        cur.execute("DELETE FROM order_items WHERE order_id = ?", (order_id,))
        cur.execute("DELETE FROM orders WHERE order_id = ?", (order_id,))
        
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"Ошибка в cancel_order: {e}")
        return False

# --- Регистрация функций для использования внутри SQL ---

def register_functions(conn):
    conn.create_function("CALC_DISCOUNT", 2, calc_discount)
    conn.create_function("PLURALIZE_ITEMS", 1, pluralize_items)
    conn.create_function("FORMAT_FULL_NAME", 3, format_full_name)
    conn.create_function("GET_CLIENT_TIER", 1, get_client_tier)
    conn.create_function("GET_LOYALTY_DAYS", 1, get_client_loyalty_days)