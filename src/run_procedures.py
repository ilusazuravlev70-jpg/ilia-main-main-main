from procedures_functions import register_functions, create_order, get_sales_report
import sqlite3

conn = sqlite3.connect("db/shoe_store.sqlite")
register_functions(conn) # Чтобы функции работали внутри SQL

# Тест процедуры создания заказа
success = create_order(conn, user_id=1, stock_item_id=1, quantity=2)
print(f"Заказ создан: {success}")

# Тест отчета
print(get_sales_report(conn, '2026-10-01', '2026-10-27'))

conn.close()