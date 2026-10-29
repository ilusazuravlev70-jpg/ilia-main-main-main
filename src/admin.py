import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "db" / "shoe_store.sqlite"

# Словарь прав доступа
PERMISSIONS = {
    "admin_db": ["SELECT", "INSERT", "UPDATE", "DELETE", "CREATE", "DROP"],
    "developer": ["SELECT", "INSERT", "UPDATE"],
    "reader": ["SELECT"]
}

def check_permission(conn, user_id, action):
    cur = conn.cursor()
    cur.execute("SELECT role_name FROM users u JOIN roles r ON u.role_id = r.role_id WHERE u.user_id = ?", (user_id,))
    row = cur.fetchone()
    if not row:
        return False
    
    role_name = row[0]
    allowed_actions = PERMISSIONS.get(role_name, [])
    
    return action.upper() in allowed_actions

# Тестирование
if __name__ == "__main__":
    conn = sqlite3.connect(DB_PATH)
    # Предположим, user_id 1 - админ, user_id 3 - читатель
    print("Админ может DELETE:", check_permission(conn, 1, "DELETE"))  # True
    print("Читатель может DELETE:", check_permission(conn, 3, "DELETE")) # False
    conn.close()