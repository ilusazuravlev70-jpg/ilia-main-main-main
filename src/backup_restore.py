import sqlite3
import shutil
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).parent.parent / "db" / "shoe_store.sqlite"
BACKUP_DIR = Path(__file__).parent.parent / "db" / "backups"

def backup_simple():
    BACKUP_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M")
    backup_path = BACKUP_DIR / f"backup_{timestamp}.sqlite"
    shutil.copy(DB_PATH, backup_path)
    print(f"Бэкап создан (shutil): {backup_path}")

def backup_safe():
    BACKUP_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M")
    backup_path = BACKUP_DIR / f"safe_backup_{timestamp}.sqlite"
    
    with sqlite3.connect(DB_PATH) as src_conn:
        with sqlite3.connect(backup_path) as dst_conn:
            src_conn.backup(dst_conn)
    print(f"Бэкап создан (safe): {backup_path}")

def check_integrity():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("PRAGMA integrity_check;")
    result = cur.fetchone()[0]
    conn.close()
    return result

def get_db_stats():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    cur.execute("PRAGMA page_size;")
    page_size = cur.fetchone()[0]
    
    cur.execute("PRAGMA page_count;")
    page_count = cur.fetchone()[0]
    
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cur.fetchall()]
    
    conn.close()
    return {
        "size_bytes": page_size * page_count,
        "page_size": page_size,
        "page_count": page_count,
        "tables": tables
    }

def restore(backup_path):
    if Path(backup_path).exists():
        shutil.copy(backup_path, DB_PATH)
        print(f"База восстановлена из {backup_path}")
    else:
        print("Файл бэкапа не найден.")