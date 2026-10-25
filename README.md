# 📦 E-Commerce Delivery Performance Analytics

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![SQL](https://img.shields.io/badge/SQL-SQLite-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-red.svg)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Wrangling-purple.svg)

## 📌 Executive Summary

Proyek _end-to-end data analytics_ untuk mengevaluasi performa pengiriman pada dataset publik Olist (E-Commerce Brasil) yang berisi **96.470 pesanan**. Analisis mencakup ketepatan waktu pengiriman (OTD), durasi, tren bulanan, perbedaan wilayah, dan hubungan antara keterlambatan pengiriman dengan skor ulasan pelanggan.

**🔗 [KLIK DI SINI UNTUK MELIHAT LIVE DASHBOARD](https://cahyokml-delivery-analytics.streamlit.app/)**

### 💡 Key Insights (Golden Findings)

1. **Keterlambatan Menghancurkan Reputasi:** Pesanan yang terlambat memiliki rata-rata skor ulasan **2.57**, turun drastis dibandingkan pesanan tepat waktu yang mendapat **4.29**. Hal ini membuktikan keterlambatan berdampak langsung pada _churn_ dan reputasi.
2. **Kesenjangan Geografis:** Meskipun OTD rate keseluruhan sangat baik (**91.89%**), keterlambatan sangat terkonsentrasi di wilayah tertentu seperti **AL (23.93%)** dan **MA (19.67%)**.
3. **Efisiensi Pengiriman:** Secara umum, logistik Olist tiba rata-rata **11.18 hari lebih awal** dari estimasi. Namun, **7.826 pesanan** yang terlambat tetap menjadi prioritas utama untuk diperbaiki.

---

## 🛠️ Tech Stack & Data Pipeline

- **Data Engineering (Python/Pandas):** Membersihkan 9 tabel mentah menjadi 1 tabel fakta (`fact_orders.csv`) dengan validasi relasi _one-to-one_ dan penanganan data duplikat.
- **Analytical SQL (SQLite):** Menulis 12+ _complex queries_ menggunakan CTE dan Window Functions untuk mengekstraksi _insight_ bisnis.
- **Interactive Dashboard (Streamlit & Plotly):** Membangun UI/UX interaktif dengan tema _Dark Mode & Glassmorphism_, lengkap dengan _Dynamic Insights_.

---

## 📂 Project Structure

```text
Delivery-Performance-Analytics/
├── data/
│   ├── raw/                  # Dataset asli Olist (Kaggle)
│   ├── processed/            # Dataset bersih (fact_orders.csv) & Database (olist.db)
├── src/
│   ├── 01_data_audit.py      # Script audit kualitas data (missing values, duplikat)
│   └── 02_clean_merge.py     # Script agregasi 9 tabel & perhitungan metrik (OTD, Late)
├── sql/
│   ├── 01_load_to_db.py      # Script memuat CSV ke SQLite
│   ├── 02_analysis_queries.sql # Kumpulan query analisis bisnis
│   └── 03_run_queries.py     # Script eksekusi query & simpan hasil ke CSV
├── dashboard/
│   └── app.py                # Kode aplikasi Streamlit UI/UX
├── reports/
│   ├── figures/              # Output visualisasi gambar
│   └── tables/               # Output hasil query SQL (CSV)
└── requirements.txt
```
