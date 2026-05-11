import sqlite3

DB_NAME = "users.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            chat_id INTEGER,
            user_id INTEGER,
            name TEXT,
            UNIQUE(chat_id, user_id)
        )
    """)

    conn.commit()
    conn.close()


def add_user(chat_id: int, user_id: int, name: str):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        INSERT OR IGNORE INTO users (chat_id, user_id, name)
        VALUES (?, ?, ?)
    """, (chat_id, user_id, name))

    conn.commit()
    conn.close()


def get_users(chat_id: int):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        SELECT name FROM users
        WHERE chat_id = ?
    """, (chat_id,))

    rows = cur.fetchall()

    conn.close()

    return [r[0] for r in rows]
