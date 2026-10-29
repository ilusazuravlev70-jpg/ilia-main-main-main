import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "db" / "shoe_store.sqlite"

# --- БЛОК 1. Функции (Калькуляторы) ---

def calc_order_total(price, quantity):
    if price is None or quantity is None:
        return 0.0
    if quantity <= 0:
        return 0.0
    return round(price * quantity, 2)

def get_category_count(conn, category_name):
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM products WHERE category = ?", (category_name,))
    result = cur.fetchone()[0]
    return result if result is not None else 0

def format_phone(phone):
    if not phone or not isinstance(phone, str):
        return phone
    digits = ''.join(filter(str.isdigit, phone))
    if len(digits) == 11 and digits.startswith('8'):
        digits = '7' + digits[1:]
    if len(digits) == 11:
        return f"+{digits[0]} ({digits[1:4]}) {digits[4:7]}-{digits[7:9]}-{digits[9:11]}"
    return phone

# --- БЛОК 2. Эмуляция процедур (Транзакции) ---

def create_order(conn, user_id, stock_item_id, quantity):
    try:
        cur = conn.cursor()
        
        # 1. Проверка остатка
        cur.execute("SELECT quantity_available FROM stock_items WHERE stock_item_id = ?", (stock_item_id,))
        row = cur.fetchone()
        if not row or row[0] < quantity:
            print("Ошибка: Недостаточно товара на складе.")
            return False
            
        # 2. Вставка в orders
        cur.execute("INSERT INTO orders (order_date, user_id) VALUES (?, ?)", 
                    (datetime.now().strftime("%Y-%m-%d"), user_id))
        order_id = cur.lastrowid
        
        # 3. Получение цены товара
        cur.execute("SELECT price FROM stock_items WHERE stock_item_id = ?", (stock_item_id,))
        price = cur.fetchone()[0]
        
        # 4. Вставка в order_items
        cur.execute("INSERT INTO order_items (order_id, stock_item_id, quantity, price) VALUES (?, ?, ?, ?)", 
                    (order_id, stock_item_id, quantity, price))
        
        # 5. Списание остатка (вызовем отдельную процедуру для чистоты)
        update_stock(conn, stock_item_id, quantity)
        
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"Ошибка создания заказа: {e}")
        return False

def update_stock(conn, stock_item_id, quantity_sold):
    try:
        cur = conn.cursor()
        cur.execute("UPDATE stock_items SET quantity_available = quantity_available - ? WHERE stock_item_id = ?", 
                    (quantity_sold, stock_item_id))
        
        # Проверка на отрицательный остаток
        cur.execute("SELECT quantity_available FROM stock_items WHERE stock_item_id = ?", (stock_item_id,))
        if cur.fetchone()[0] < 0:
            raise ValueError("Остаток ушел в минус!")
            
        return True
    except Exception as e:
        conn.rollback()
        print(f"Ошибка обновления остатков: {e}")
        return False

def get_sales_report(conn, start_date, end_date):
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT SUM(oi.quantity * oi.price) 
            FROM orders o
            JOIN order_items oi ON o.order_id = oi.order_id
            WHERE o.order_date BETWEEN ? AND ?
        """, (start_date, end_date))
        
        total = cur.fetchone()[0] or 0.0
        return f"С {start_date} по {end_date} продано товаров на сумму {total:.2f} руб."
    except Exception as e:
        print(f"Ошибка отчета: {e}")
        return None

# --- Регистрация функций для использования внутри SQL (аналогично прошлому дню) ---

def register_functions(conn):
    conn.create_function("CALC_ORDER_TOTAL", 2, calc_order_total)
    conn.create_function("FORMAT_PHONE", 1, format_phone)