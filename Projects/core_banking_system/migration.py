from dotenv import load_dotenv
import os
import sys
import mysql.connector
from datetime import datetime
import glob

# Load .env environment variables
load_dotenv()

def get_db_config():
    return {
        'user': os.getenv('DB_USERNAME'),
        'password': os.getenv('DB_PASSWORD'),
        'host': os.getenv('DB_HOST'),
        'port': os.getenv('DB_PORT'),
        'database': os.getenv('DB_DATABASE')
    }

def init_migrations_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS migrations (
            id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL
        )
    """)

def generate(name):
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    filename = f"migrations/{timestamp}_{name}.sql"
    os.makedirs('migrations', exist_ok=True)
    open(filename, 'a').close()
    print(f"✅ Created migration: {filename}")

def migrate():
    print("🔗 Connecting to DB with config:", get_db_config())
    db = mysql.connector.connect(**get_db_config())
    cursor = db.cursor()
    init_migrations_table(cursor)

    # Fetch already executed migrations
    cursor.execute("SELECT name FROM migrations")
    executed_migrations = [name for (name,) in cursor.fetchall()]

    # Find and sort migration SQL files
    migration_files = sorted(glob.glob("migrations/*.sql"))

    for file_path in migration_files:
        filename = os.path.basename(file_path)
        if filename not in executed_migrations:
            print(f"🚀 Running migration: {filename}")
            with open(file_path, 'r') as f:
                sql = f.read()
                for statement in sql.split(';'):
                    statement = statement.strip()
                    if statement:
                        cursor.execute(statement)

            # Record this migration as executed
            cursor.execute("INSERT INTO migrations (name) VALUES (%s)", (filename,))
            db.commit()
            print(f"✅ Executed: {filename}")

    cursor.close()
    db.close()
    print("🎉 All migrations completed.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python migration.py [generate|migrate] <migration_name?>")
        sys.exit(1)

    command = sys.argv[1]
    if command == "generate":
        if len(sys.argv) != 3:
            print("Usage: python migration.py generate <migration_name>")
            sys.exit(1)
        generate(sys.argv[2])
    elif command == "migrate":
        migrate()
    else:
        print("❌ Invalid command. Use 'generate' or 'migrate'")
