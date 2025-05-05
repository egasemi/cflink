from flask import g

from dotenv import load_dotenv

import os

import libsql_experimental as libsql

load_dotenv()

TURSO_DATABASE_URL = os.environ.get("TURSO_DATABASE_URL")
TURSO_AUTH_TOKEN = os.environ.get("TURSO_AUTH_TOKEN")


def get_db():
    if 'db' not in g:
"""         try:
            g.db = libsql.connect(
                "local.db",
                sync_url=TURSO_DATABASE_URL,
                auth_token=TURSO_AUTH_TOKEN
            )
        except Exception as e:
            print("⚠️ Error al conectar con Turso, usando solo base local:", e)
            g.db = libsql.connect("local.db") """
        g.db = libsql.connect("local.db")
    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
"""     db = get_db() """
    create_tables()
"""     try:
        db.sync()
    except Exception as e:
        print("⚠️ No se pudo sincronizar con Turso:", e) """

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
        );
    ''')
    db.commit()