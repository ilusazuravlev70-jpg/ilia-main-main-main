import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "db" / "shoe_store.sqlite"
SCHEMA_PATH = Path(__file__).parent.parent / "db" / "schema.sql"

def main():
    conn = sqlite3.connect(DB_PATH)
    try:
        # Получаем список всех SQL-команд, которые создают текущую структуру
        schema_script = conn.execute("SELECT sql FROM sqlite_master WHERE sql IS NOT NULL ORDER BY tbl_name, type DESC;").fetchall()
        
        with open(SCHEMA_PATH, "w", encoding="utf-8") as f:
            for row in schema_script:
                f.write(row[0] + ";\n\n")  # Добавляем точку с запятой и пустую строку для читаемости
                
        print(f"Структура базы успешно экспортирована в {SCHEMA_PATH}")
        
    except sqlite3.Error as e:
        print(f"Ошибка при экспорте структуры: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    main()