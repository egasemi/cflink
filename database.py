from flask import g
import sqlite3

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect("local.db")
        g.db.row_factory = sqlite3.Row  # Para poder acceder a columnas por nombre
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    create_tables()

def create_tables():
    db = get_db()
    db.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user'
        )
    ''')
    db.execute('''
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_url TEXT NOT NULL,
            short_url TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    db.execute('''
        CREATE TABLE IF NOT EXISTS link_visits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            short_url VARCHAR(255),
            original_url VARCHAR(255),
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            user_agent VARCHAR(255),
            ip_address VARCHAR(45),
            browser VARCHAR(255),
            os VARCHAR(255),
            device VARCHAR(255),
            referrer VARCHAR(255)
        )
    ''')
    db.commit()
