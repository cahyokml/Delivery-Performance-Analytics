import sqlite3
import pandas as pd
import os

# Path ke data dan database
CSV_PATH = 'data/processed/fact_orders.csv'
DB_PATH = 'data/olist.db'

print("=== MEMUAT DATA KE DATABASE SQLITE ===")

# 1. Cek apakah file CSV ada
if not os.path.exists(CSV_PATH):
    print(f"[ERROR] File {CSV_PATH} tidak ditemukan. Jalankan script 02_clean_merge.py dulu!")
else:
    # 2. Load CSV
    df = pd.read_csv(CSV_PATH)
    
    # 3. Buat koneksi ke SQLite dan masukkan data
    conn = sqlite3.connect(DB_PATH)
    df.to_sql('fact_orders', conn, if_exists='replace', index=False)
    
    # 4. Test query sederhana
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM fact_orders")
    row_count = cursor.fetchone()[0]
    
    conn.close()
    
    print(f"[SUKSES] {row_count} baris data berhasil dimuat ke database: {DB_PATH}")
    print(f"Tabel 'fact_orders' siap dianalisis menggunakan SQL.")