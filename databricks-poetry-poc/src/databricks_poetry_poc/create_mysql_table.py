import json
import mysql.connector
from mysql.connector import Error

def read_json_mapping(path):
    with open(path, "r") as f:
        return json.load(f)

def create_mysql_table(mapping):
    try:
        print("🔌 Connecting to MySQL...")

        # Try to connect with timeout
        conn = mysql.connector.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="root",
            database="ecvs",
            connection_timeout=5
        )

        print("🚀 After connection attempt")

        if conn.is_connected():
            print("✅ Connected to MySQL!")
        else:
            print("❌ Connection failed.")
            return

        cursor = conn.cursor()

        table_name = mapping["table_name"]
        columns = mapping["columns"]

        ddl = f"CREATE TABLE IF NOT EXISTS {table_name} (" + ", ".join([f"{col['name']} {col['type']}" for col in columns]) + ");"
        print("📝 Running DDL:\n", ddl)

        cursor.execute(ddl)
        print(f"✅ Table `{table_name}` created successfully!")

        conn.commit()
        cursor.close()
        conn.close()

    except Error as err:
        print(f"❌ MySQL Error: {err}")
    except Exception as e:
        print(f"❌ General Error: {e}")

if __name__ == "__main__":
    mapping = read_json_mapping("mappings/mysql_table_schema.json")
    create_mysql_table(mapping)
