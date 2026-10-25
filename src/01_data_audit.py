import pandas as pd
import os

# 1. Tentukan Path
RAW_DATA_DIR = 'data/raw/'
REPORTS_DIR = 'reports/tables/'

# Buat folder reports/tables jika belum ada
os.makedirs(REPORTS_DIR, exist_ok=True)

# Daftar file yang akan diaudit
files = {
    'customers': 'olist_customers_dataset.csv',
    'orders': 'olist_orders_dataset.csv',
    'order_items': 'olist_order_items_dataset.csv',
    'payments': 'olist_order_payments_dataset.csv',
    'reviews': 'olist_order_reviews_dataset.csv',
    'products': 'olist_products_dataset.csv',
    'sellers': 'olist_sellers_dataset.csv',
    'geolocation': 'olist_geolocation_dataset.csv'
}

print("=== MEMULAI DATA AUDIT ===\n")
summary_data = []
dataframes = {}

# 2. Audit Dasar (Shape, Missing Values, Duplikat)
for name, filename in files.items():
    filepath = os.path.join(RAW_DATA_DIR, filename)
    if os.path.exists(filepath):
        df = pd.read_csv(filepath)
        dataframes[name] = df
        
        # Hitung metrik
        rows, cols = df.shape
        missing = df.isnull().sum().sum()
        duplicates = df.duplicated().sum()
        
        summary_data.append({
            'Table': name,
            'Rows': rows,
            'Columns': cols,
            'Total Missing Values': missing,
            'Total Duplicates': duplicates
        })
        
        print(f"[OK] {name}: {rows} baris, {cols} kolom.")
    else:
        print(f"[WARNING] File {filename} tidak ditemukan di {RAW_DATA_DIR}")

# 3. Simpan Ringkasan ke CSV
summary_df = pd.DataFrame(summary_data)
summary_df.to_csv(os.path.join(REPORTS_DIR, 'data_audit_summary.csv'), index=False)
print(f"\n[SUKSES] Ringkasan audit disimpan di {REPORTS_DIR}data_audit_summary.csv")

# 4. Cek Integritas Relasi (Referential Integrity)
print("\n=== CEK INTEGRITAS RELASI ===")
orders = dataframes['orders']
customers = dataframes['customers']
order_items = dataframes['order_items']

# Cek apakah semua customer_id di orders ada di tabel customers
invalid_customer = ~orders['customer_id'].isin(customers['customer_id'])
print(f"Order dengan customer_id tidak valid: {invalid_customer.sum()}")

# Cek apakah semua order_id di order_items ada di tabel orders
invalid_order = ~order_items['order_id'].isin(orders['order_id'])
print(f"Item dengan order_id tidak valid: {invalid_order.sum()}")

# 5. Cek Anomali Logika Bisnis
print("\n=== CEK ANOMALI BISNIS ===")
# Konversi tanggal ke datetime untuk pengecekan
orders['order_delivered_customer_date'] = pd.to_datetime(orders['order_delivered_customer_date'], errors='coerce')
orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'], errors='coerce')

# Kasus 1: Status delivered tapi tanggal pengiriman kosong
delivered_no_date = orders[(orders['order_status'] == 'delivered') & (orders['order_delivered_customer_date'].isnull())]
print(f"Order berstatus 'delivered' tapi tanpa tanggal pengiriman: {len(delivered_no_date)}")

# Kasus 2: Tanggal terima lebih awal dari tanggal beli
invalid_date = orders[orders['order_delivered_customer_date'] < orders['order_purchase_timestamp']]
print(f"Order dengan tanggal terima lebih awal dari tanggal beli: {len(invalid_date)}")

print("\n=== AUDIT SELESAI ===")