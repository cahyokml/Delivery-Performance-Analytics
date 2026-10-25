# 📦 E-Commerce Delivery Performance Analytics

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![SQL](https://img.shields.io/badge/SQL-SQLite-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-red.svg)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Wrangling-purple.svg)

## 📌 Executive Summary
Proyek ini adalah **end-to-end data analytics pipeline** terhadap **96.470 pesanan** dari dataset publik Olist (E-Commerce Brasil). Tujuan utamanya adalah mengukur performa *On-Time Delivery* (OTD), mengidentifikasi akar masalah keterlambatan logistik, dan mengkuantifikasi dampaknya terhadap kepuasan pelanggan (Customer Satisfaction).

**🔗 [KLIK DI SINI UNTUK MELIHAT LIVE DASHBOARD](https://cahyokml-delivery-analytics.streamlit.app/)**

### 💡 Key Insights (Golden Findings)
1. **Keterlambatan Menghancurkan Reputasi:** Pesanan yang terlambat memiliki rata-rata skor ulasan **2.57**, turun drastis dibandingkan pesanan tepat waktu yang mendapat **4.29**. Hal ini membuktikan keterlambatan berdampak langsung pada *churn* dan reputasi.
2. **Kesenjangan Geografis:** Meskipun OTD rate keseluruhan sangat baik (**91.89%**), keterlambatan sangat terkonsentrasi di wilayah tertentu seperti **AL (23.93%)** dan **MA (19.67%)**.
3. **Efisiensi Pengiriman:** Secara umum, logistik Olist tiba rata-rata **11.88 hari lebih awal** dari estimasi. Namun, 7.826 pesanan yang terlambat tetap menjadi prioritas utama untuk diperbaiki.

---

## 🛠️ Tech Stack & Data Pipeline
- **Data Cleaning & Engineering:** Python (Pandas, Numpy) — Membersihkan 9 tabel mentah menjadi 1 tabel fakta (`fact_orders.csv`).
- **Analytical SQL:** SQLite — Menulis 12+ *complex queries* menggunakan CTE dan Window Functions untuk mengekstraksi *insight* bisnis.
- **Interactive Dashboard:** Streamlit & Plotly — Membangun UI/UX interaktif dengan tema *Dark Mode & Glassmorphism*.

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
│   └── app.py                # Kode aplikasi Streamlit
├── reports/
│   ├── figures/              # Output visualisasi gambar
│   └── tables/               # Output hasil query SQL (CSV)
└── requirements.txt