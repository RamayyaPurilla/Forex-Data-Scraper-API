import sqlite3

def get_db_connection():
    conn = sqlite3.connect('forex_data.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS forex_rates (
            from_currency TEXT,
            to_currency TEXT,
            date DATE,
            rate REAL,
            PRIMARY KEY (from_currency, to_currency, date)
        )
    ''')
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()


