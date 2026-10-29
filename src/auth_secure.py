import sqlite3
import hashlib
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).parent.parent / "db" / "shoe_store.sqlite"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(login, password):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    password_hash = hash_password(password)
    try:
        cur.execute("INSERT INTO users (login, password_hash) VALUES (?, ?)", (login, password_hash))
        conn.commit()
        print("Пользователь зарегистрирован.")
    except sqlite3.IntegrityError:
        print("Логин занят.")
    finally:
        conn.close()

def check_password(login, password):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    # Логирование попытки входа
    cur.execute("INSERT INTO login_audit (login, status, login_time) VALUES (?, 'ATTEMPT', datetime('now'))")
    
    cur.execute("SELECT password_hash FROM users WHERE login = ?", (login,))
    row = cur.fetchone()
    
    if row and row[0] == hash_password(password):
        cur.execute("UPDATE login_audit SET status = 'SUCCESS' WHERE login_time = (SELECT MAX(login_time) FROM login_audit WHERE login = ?)", (login,))
        conn.commit()
        conn.close()
        return True
    else:
        cur.execute("UPDATE login_audit SET status = 'FAIL' WHERE login_time = (SELECT MAX(login_time) FROM login_audit WHERE login = ?)", (login,))
        conn.commit()
        conn.close()
        return False

# Инициализация таблицы login_audit (выполнить один раз)
def init_audit_table():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS login_audit (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login TEXT NOT NULL,
            status TEXT NOT NULL,
            login_time TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_audit_table()
    # register_user("testuser", "qwerty123")
    print("Вход успешен:", check_password("testuser", "qwerty123"))
    print("Вход успешен (неверный пароль):", check_password("testuser", "wrongpass"))