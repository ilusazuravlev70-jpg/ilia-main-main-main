import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "db" / "shoe_store.sqlite"

def test_triggers():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    try:
        # 1. Подготовка: берем существующий товар и складскую позицию
        cur.execute("SELECT stock_item_id, quantity_available FROM stock_items LIMIT 1")
        stock_item_id, old_quantity = cur.fetchone()
        
        cur.execute("SELECT product_id FROM stock_items WHERE stock_item_id = ?", (stock_item_id,))
        product_id = cur.fetchone()[0]
        
        cur.execute("SELECT user_id FROM users LIMIT 1")
        user_id = cur.fetchone()[0]

        print(f"--- Шаг 1: Исходный остаток на складе (ID {stock_item_id}): {old_quantity} ---")

        # 2. Создаем заказ
        cur.execute("INSERT INTO orders (order_date, user_id) VALUES (datetime('now'), ?)", (user_id,))
        order_id = cur.lastrowid
        
        # 3. Добавляем товар в заказ (должен сработать триггер списания остатков)
        quantity_to_buy = 2
        cur.execute("INSERT INTO order_items (order_id, stock_item_id, quantity, price) VALUES (?, ?, 2, (SELECT price FROM products WHERE product_id = ?))", 
                    (order_id, stock_item_id, product_id))
        
        # 4. Проверяем остаток
        cur.execute("SELECT quantity_available FROM stock_items WHERE stock_item_id = ?", (stock_item_id,))
        new_quantity = cur.fetchone()[0]
        
        print(f"--- Шаг 2: Остаток после добавления в заказ: {new_quantity} ---")
        print(f"Результат триггера списания: {'ОК' if new_quantity == old_quantity - quantity_to_buy else 'ОШИБКА'} \n")

        # 5. Проверка триггера-защиты (попытка удалить пользователя с заказом)
        print("--- Шаг 3: Попытка удалить пользователя с заказом ---")
        try:
            cur.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
            print("ОШИБКА: Пользователь удалился, триггер не сработал!")
        except sqlite3.IntegrityError as e:
            print(f"ОК: Триггер защиты сработал. Ошибка: {e}")

        # 6. Проверка триггера аудита цен
        print("\n--- Шаг 4: Изменение цены товара (для аудита) ---")
        cur.execute("UPDATE products SET price = price + 100 WHERE product_id = ?", (product_id,))
        
        cur.execute("SELECT table_name, operation, old_value, new_value FROM audit_log ORDER BY log_id DESC LIMIT 1")
        log_entry = cur.fetchone()
        print(f"Запись в логе: Таблица '{log_entry[0]}', Действие '{log_entry[1]}', Было '{log_entry[2]}', Стало '{log_entry[3]}'")

        conn.commit()
        
    except Exception as e:
        conn.rollback()
        print(f"Произошла ошибка в тесте: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    test_triggers()