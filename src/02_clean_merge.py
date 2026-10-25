
import pandas as pd
import os

RAW_DIR = "data/raw/"
PROCESSED_DIR = "data/processed/"
os.makedirs(PROCESSED_DIR, exist_ok=True)

print("=== MEMULAI CLEANING & MERGE ===")

# 1. Load data utama
orders = pd.read_csv(os.path.join(RAW_DIR, "olist_orders_dataset.csv"))
order_items = pd.read_csv(os.path.join(RAW_DIR, "olist_order_items_dataset.csv"))
payments = pd.read_csv(os.path.join(RAW_DIR, "olist_order_payments_dataset.csv"))
reviews = pd.read_csv(os.path.join(RAW_DIR, "olist_order_reviews_dataset.csv"))
customers = pd.read_csv(os.path.join(RAW_DIR, "olist_customers_dataset.csv"))

# 2. Filter pesanan delivered dan konversi tanggal
orders = orders.loc[orders["order_status"] == "delivered"].copy()

date_cols = [
    "order_purchase_timestamp",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
]

for col in date_cols:
    orders[col] = pd.to_datetime(orders[col], errors="coerce")

# Hanya pesanan dengan seluruh tanggal wajib tersedia
orders = orders.dropna(subset=date_cols).copy()

# 3. Hitung metrik pengiriman
actual = orders["order_delivered_customer_date"]
estimated = orders["order_estimated_delivery_date"]

orders["delivery_days"] = (
    actual - orders["order_purchase_timestamp"]
).dt.total_seconds() / 86400

orders["delay_days"] = (
    actual - estimated
).dt.total_seconds() / 86400

orders["is_late"] = orders["delay_days"] > 0
orders["is_on_time"] = ~orders["is_late"]

# Hapus durasi pengiriman negatif dan catat jumlahnya
invalid_delivery = orders["delivery_days"] < 0
print(f"Durasi pengiriman negatif: {invalid_delivery.sum()}")

orders = orders.loc[~invalid_delivery].copy()

# 4. Agregasi item per pesanan
items_agg = order_items.groupby("order_id").agg(
    total_items=("order_item_id", "count"),
    total_price=("price", "sum"),
    total_freight=("freight_value", "sum"),
).reset_index()

# 5. Agregasi pembayaran per pesanan
payments_agg = payments.groupby("order_id").agg(
    total_payment=("payment_value", "sum"),
    payment_type=("payment_type", "first"),
).reset_index()

# 6. Pilih satu review terbaru per pesanan
reviews["review_creation_date"] = pd.to_datetime(
    reviews["review_creation_date"], errors="coerce"
)

reviews_agg = (
    reviews.sort_values(
        ["review_creation_date", "review_answer_timestamp"],
        na_position="first",
    )
    .drop_duplicates(subset=["order_id"], keep="last")
    [["order_id", "review_score"]]
)

# 7. Merge dengan validasi relasi satu-ke-satu
df = orders.merge(
    customers[["customer_id", "customer_state"]].drop_duplicates("customer_id"),
    on="customer_id",
    how="left",
    validate="many_to_one",
)

df = df.merge(
    items_agg, on="order_id", how="left", validate="one_to_one"
)
df = df.merge(
    payments_agg, on="order_id", how="left", validate="one_to_one"
)
df = df.merge(
    reviews_agg, on="order_id", how="left", validate="one_to_one"
)

# 8. Pilih kolom akhir
final_cols = [
    "order_id", "customer_id", "customer_state",
    "order_purchase_timestamp",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
    "delivery_days", "delay_days", "is_late", "is_on_time",
    "total_items", "total_price", "total_freight",
    "total_payment", "payment_type", "review_score",
]

fact_orders = df[final_cols].copy()

# 9. Validasi hasil
print(f"Jumlah order_id duplikat: {fact_orders['order_id'].duplicated().sum()}")
print(f"Total baris: {len(fact_orders)}")
print(f"Total terlambat: {fact_orders['is_late'].sum()}")
print(f"Total tepat waktu: {fact_orders['is_on_time'].sum()}")
print(f"Rata-rata durasi pengiriman: {fact_orders['delivery_days'].mean():.2f} hari")
print(f"Rata-rata keterlambatan: {fact_orders['delay_days'].mean():.2f} hari")
print("\nNilai kosong:")
print(fact_orders.isna().sum())

# Simpan hasil
output_path = os.path.join(PROCESSED_DIR, "fact_orders.csv")
fact_orders.to_csv(output_path, index=False)

print(f"\n[SUKSES] Data tersimpan di: {output_path}")
print("=== PROSES SELESAI ===")
