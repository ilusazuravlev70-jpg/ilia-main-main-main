from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "db" / "shoe_store.sqlite"

def main():
    if DB_PATH.exists():
        DB_PATH.unlink()
        print(f"База данных {DB_PATH.name} успешно удалена.")
    else:
        print("Файл базы данных не найден.")

if __name__ == "__main__":
    main()