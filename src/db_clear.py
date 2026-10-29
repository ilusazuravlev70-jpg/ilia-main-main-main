import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "db" / "shoe_store.sqlite"

def main():
    conn = sqlite3.connect(DB_PATH)
    try:
        # Включаем проверку внешних ключей, чтобы удаление шло в правильном порядке
        conn.execute("PRAGMA foreign_keys = ON;")
        
        # Порядок удаления данных обратный порядку создания таблиц
        tables = [
            "order_items", 
            "orders", 
            "stock_items", 
            "users", 
            "products", 
            "sizes", 
            "roles"
        ]
        
        for table in tables:
            conn.execute(f"DELETE FROM {table};")
            
        conn.commit()
        print("Все данные из таблиц успешно удалены. Структура базы сохранена.")
        
    except sqlite3.Error as e:
        conn.rollback()
        print(f"Ошибка при очистке данных: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    main()