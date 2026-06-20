import sqlite3

def get_db_connection():
    conn = sqlite3.connect('guestbook.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Таблица сообщений (ПР №9)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT EXISTS,
            name TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_DATE
        )
    ''')
    
    # Таблица пользователей (ПР №12)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    
    # Стандартный админ
    cursor.execute('SELECT * FROM users WHERE username = ?', ('admin',))
    if not cursor.fetchone():
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', ('admin', '123'))
        
    conn.commit()
    conn.close()

def get_all_messages():
    conn = get_db_connection()
    messages = conn.execute('SELECT * FROM messages ORDER BY id DESC').fetchall()
    conn.close()
    return messages

def add_message(name, message):
    conn = get_db_connection()
    conn.execute('INSERT INTO messages (name, message) VALUES (?, ?)', (name, message))
    conn.commit()
    conn.close()

def get_message_count():
    conn = get_db_connection()
    count = conn.execute('SELECT COUNT(*) FROM messages').fetchone()[0]
    conn.close()
    return count

def delete_message(message_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM messages WHERE id = ?', (message_id,))
    conn.commit()
    conn.close()
