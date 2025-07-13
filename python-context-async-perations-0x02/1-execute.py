import sqlite3

class ExecuteQuery:
    def __init__(self, db_name, query, params=()):
        self.db_name = db_name
        self.query = query
        self.params = params
        self.connection = None
        self.cursor = None
        self.result = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        self.cursor.execute(self.query, self.params)
        self.result = self.cursor.fetchall()
        return self.result  # Passed to the `as` part in the with block

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

# --- Setup Demo Database (run only once or reset table) ---
def setup_demo_db():
    with sqlite3.connect("example.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS users")
        cursor.execute("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY,
                name TEXT,
                age INTEGER
            )
        """)
        cursor.executemany(
            "INSERT INTO users (name, age) VALUES (?, ?)",
            [
                ("Alice", 22),
                ("Bob", 30),
                ("Charlie", 27),
                ("Diana", 19)
            ]
        )
        conn.commit()

setup_demo_db()

# --- Use the ExecuteQuery Context Manager ---
query = "SELECT * FROM users WHERE age > ?"
params = (25,)

with ExecuteQuery("example.db", query, params) as results:
    for row in results:
        print(row)