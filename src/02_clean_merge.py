import pandas as pd
import os

RAW_DIR = 'data/raw/'
PROCESSED_DIR = 'data/processed/'
os.makedirs(PROCESSED_DIR, exist_ok=True)

print("=== MEMULAI CLEANING & MERGE ===")

# 1. Load Data Utama
orders = pd.read_csv(os.path.join(RAW_DIR, 'olist_orders_dataset.csv'))
order_items = pd.read_csv(os.path.join(RAW_DIR, 'olist_order_items_dataset.csv'))
payments = pd.read_csv(os.path.join(RAW_DIR, 'olist_order_payments_dataset.csv'))
reviews = pd.read_csv(os.path.join(RAW_DIR, 'olist_order_reviews_dataset.csv'))
customers = pd.read_csv(os.path.join(RAW_DIR, 'olist_customers_dataset.csv'))

# 2. Cleaning & Konversi Tanggal (Orders)
# Kita hanya fokus pada pesanan yang statusnya 'delivered' (terkirim) untuk analisis performa
orders = orders[orders['order_status'] == 'delivered'].copy()

date_cols = [
    'order_purchase_timestamp', 
    'order_approved_at', 
    'order_delivered_carrier_date', 
    'order_delivered_customer_date', 
    'order_estimated_delivery_date'
]
for col in date_cols:
    orders[col] = pd.to_datetime(orders[col], errors='coerce')

# Drop baris yang tidak punya tanggal sampai di customer (karena tidak bisa dihitung performanya)
orders = orders.dropna(subset=['order_delivered_customer_date'])

# 3. Hitung Metrik Pengiriman
# delivery_days: total hari dari beli sampai terima
orders['delivery_days'] = (orders['order_delivered_customer_date'] - orders['order_purchase_timestamp']).dt.days
# delay_days: selisih hari antara aktual terima vs estimasi
orders['delay_days'] = (orders['order_delivered_customer_date'] - orders['order_estimated_delivery_date']).dt.days

# Tentukan On-Time atau Late
orders['is_late'] = orders['delay_days'] > 0
orders['is_on_time'] = orders['delay_days'] <= 0

# 4. Agregasi Tabel Lain (Level Order)
# Hitung total item & total harga per order_id
items_agg = order_items.groupby('order_id').agg(
    total_items=('order_item_id', 'count'),
    total_price=('price', 'sum'),
    total_freight=('freight_value', 'sum')
).reset_index()

# Ambil total pembayaran & tipe pembayaran utama
payments_agg = payments.groupby('order_id').agg(
    total_payment=('payment_value', 'sum'),
    payment_type=('payment_type', 'first')
).reset_index()

# Ambil skor review
reviews_agg = reviews[['order_id', 'review_score']].drop_duplicates(subset=['order_id'])

# 5. MERGE SEMUA DATA
df = orders.merge(customers[['customer_id', 'customer_state']], on='customer_id', how='left')
df = df.merge(items_agg, on='order_id', how='left')
df = df.merge(payments_agg, on='order_id', how='left')
df = df.merge(reviews_agg, on='order_id', how='left')

# 6. Pilih kolom yang relevan untuk disimpan
final_cols = [
    'order_id', 'customer_id', 'customer_state', 
    'order_purchase_timestamp', 'order_delivered_customer_date', 'order_estimated_delivery_date',
    'delivery_days', 'delay_days', 'is_late', 'is_on_time',
    'total_items', 'total_price', 'total_freight', 'total_payment', 'payment_type', 'review_score'
]
fact_orders = df[final_cols].copy()

# Simpan ke folder processed
output_path = os.path.join(PROCESSED_DIR, 'fact_orders.csv')
fact_orders.to_csv(output_path, index=False)

print(f"[SUKSES] Data bersih dan tergabung disimpan di: {output_path}")
print(f"Total baris data: {len(fact_orders)}")
print(f"Total pesanan terlambat (Late): {fact_orders['is_late'].sum()}")
print("=== PROSES SELESAI ===")