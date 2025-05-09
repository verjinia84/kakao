import os
import sqlite3
from dotenv import load_dotenv
import logging

load_dotenv()

DB_PATH = os.getenv("DB_PATH", "kakao.db")  # .env에서 DB_PATH를 읽고, 없으면 kakao.db 사용

logger = logging.getLogger("uvicorn")

def request_and_log_to_db(room, sender, msg, timestamp):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS http_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room TEXT,
            sender TEXT,
            msg TEXT,
            timestamp TEXT
        )
    """)
    cursor.execute("""
        INSERT INTO http_requests (room, sender, msg, timestamp)
        VALUES (?, ?, ?, ?)
    """, (room, sender, msg, timestamp))
    conn.commit()
    conn.close()
