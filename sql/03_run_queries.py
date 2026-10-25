import sqlite3
import pandas as pd
import os
import re

DB_PATH = 'data/olist.db'
SQL_FILE = 'sql/02_analysis_queries.sql'
OUTPUT_DIR = 'reports/tables/'

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Baca semua query dari file SQL
with open(SQL_FILE, 'r') as file:
    sql_script = file.read()

# HAPUS SEMUA KOMENTAR (baris yang diawali --) agar tidak mengganggu pemisahan query
sql_script_clean = re.sub(r'--.*', '', sql_script)

# Split query berdasarkan titik koma (;)
queries = [q.strip() for q in sql_script_clean.split(';') if q.strip()]

conn = sqlite3.connect(DB_PATH)

for i, query in enumerate(queries, 1):
    print(f"Menjalankan Query {i}...")
    try:
        df_result = pd.read_sql_query(query, conn)
        output_file = os.path.join(OUTPUT_DIR, f'sql_result_{i}.csv')
        df_result.to_csv(output_file, index=False)
        print(f"  -> Berhasil disimpan di {output_file}")
        # Menampilkan maksimal 3 baris pertama agar terminal tidak terlalu panjang
        print(df_result.head(3).to_string(index=False)) 
        print("-" * 40)
    except Exception as e:
        print(f"  -> Error pada Query {i}: {e}")

conn.close()
print("\n=== SEMUA QUERY SELESAI DIEKSEKUSI ===")