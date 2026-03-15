import MySQLdb
from config import DB_CONFIG


def get_connection():
    return MySQLdb.connect(
        host=DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        passwd=DB_CONFIG['password'],
        db=DB_CONFIG['database'],
        port=DB_CONFIG['port'],
        charset='utf8mb4',
    )


def fetch_all(sql, params=None):
    conn = get_connection()
    try:
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(sql, params or ())
        rows = cursor.fetchall()
        return rows
    finally:
        conn.close()


def fetch_one(sql, params=None):
    conn = get_connection()
    try:
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(sql, params or ())
        row = cursor.fetchone()
        return row
    finally:
        conn.close()


def execute(sql, params=None):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(sql, params or ())
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


def count(sql, params=None):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(sql, params or ())
        row = cursor.fetchone()
        return row[0] if row else 0
    finally:
        conn.close()
