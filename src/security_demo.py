import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "db" / "shoe_store.sqlite"

def vulnerable_login(login):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    # ОПАСНО: f-строка
    cur.execute(f"SELECT user_id, login FROM users WHERE login = '{login}'")
    user = cur.fetchone()
    conn.close()
    return user

def secure_login(login):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    # БЕЗОПАСНО: параметры
    cur.execute("SELECT user_id, login FROM users WHERE login = ?", (login,))
    user = cur.fetchone()
    conn.close()
    return user

if __name__ == "__main__":
    payload = "' OR '1'='1"
    
    print("--- УЯЗВИМЫЙ ЗАПРОС ---")
    result = vulnerable_login(payload)
    print(f"Результат взлома: {result} (Если не None - база взломана)")
    
    print("\n--- БЕЗОПАСНЫЙ ЗАПРОС ---")
    result = secure_login(payload)
    print(f"Результат: {result} (Должно быть None)")