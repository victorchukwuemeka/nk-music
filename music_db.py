import sqlite

conn = sqlite3.connect("music.db")
cursor = conn.cursor()

cursor.execute(
    "CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, title TEXT, content TEXT)"
)
conn.commit()