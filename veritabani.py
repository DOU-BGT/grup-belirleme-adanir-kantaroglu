import sqlite3
from datetime import datetime

DB_FILE = 'hrms.db'

def log(mesaj):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now}] {mesaj}")

def create_connection():
    try:
        conn = sqlite3.connect(DB_FILE)
        log(f"Veritabanına bağlantı kuruldu: {DB_FILE}")
        return conn
    except sqlite3.Error as e:
        log(f"Veritabanı bağlantı hatası: {e}")
        return None

def create_tables():
    conn = create_connection()
    if conn is None:
        log("Bağlantı sağlanamadı, tablolar oluşturulamadı!")
        return

    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')
    log("Tablo kontrolü / oluşturuldu: users")

    c.execute('''
        CREATE TABLE IF NOT EXISTS personnel (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            position TEXT NOT NULL,
            salary REAL NOT NULL
        )
    ''')
    log("Tablo kontrolü / oluşturuldu: personnel")

    c.execute('''
        CREATE TABLE IF NOT EXISTS işlem_kaydi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            işlem TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')
    log("Tablo kontrolü / oluşturuldu: işlem_kaydi")

    conn.commit()
    conn.close()
    log("Veritabanı bağlantısı kapatıldı.")

def add_personnel_to_db(name, position, salary):
    try:
        conn = create_connection()
        c = conn.cursor()
        c.execute('''
            INSERT INTO personnel (name, position, salary)
            VALUES (?, ?, ?)
        ''', (name, position, salary))
        conn.commit()
        conn.close()
        log(f"Personel eklendi: {name}, {position}, ₺{salary:.2f}")
        return True
    except Exception as e:
        log(f"Hata personel eklerken: {e}")
        return False

def get_all_personnel():
    try:
        conn = create_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM personnel ORDER BY id DESC")
        personnel = c.fetchall()
        conn.close()
        log(f"Personel listesi çekildi: {len(personnel)} kayıt")
        return personnel
    except Exception as e:
        log(f"Hata personel listesi çekerken: {e}")
        return []


