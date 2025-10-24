# tables_setup.py
from config import DB

cur = DB.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS assistants (
    id SERIAL PRIMARY KEY,
    user_id BIGINT UNIQUE,
    username TEXT,
    channel_id BIGINT,
    answers INT DEFAULT 0,
    pending INT DEFAULT 0,
    rating REAL DEFAULT 0
);
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS questions (
    id SERIAL PRIMARY KEY,
    user_id BIGINT,          -- المتربص
    assistant_id INT,
    question TEXT,
    answer TEXT,
    status TEXT DEFAULT 'pending',
    rating INT
);
""")

DB.commit()
cur.close()
print("✅ Database initialized successfully.")
