import sqlite3

def init_db():
    conn = sqlite3.connect('data/scores.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pseudo TEXT NOT NULL,
            score INTEGER NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS options (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player TEXT NOT NULL,
            fire_power REAL,
            speed REAL,
            rotation_speed REAL,
            fire_delay INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def insert_score(pseudo, score):
    conn = sqlite3.connect('data/scores.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO scores (pseudo, score) VALUES (?, ?)', (pseudo, score))
    conn.commit()
    conn.close()
