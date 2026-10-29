from backup_restore import backup_safe, check_integrity, get_db_stats
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "db" / "shoe_store.sqlite"

def clear_old_logs(days=30):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM audit_log WHERE changed_at < date('now', ?)", (f'-{days} days',))
    deleted = cur.rowcount
    conn.commit()
    conn.close()
    print(f"Удалено старых логов: {deleted}")

def run_maintenance():
    print("=== Запуск обслуживания базы ===")
    print(f"Целостность: {check_integrity()}")
    backup_safe()
    stats = get_db_stats()
    print(f"Размер базы: {stats['size_bytes']} байт")
    print(f"Таблицы: {', '.join(stats['tables'])}")
    clear_old_logs()
    print("=== Обслуживание завершено ===")

if __name__ == "__main__":
    run_maintenance()