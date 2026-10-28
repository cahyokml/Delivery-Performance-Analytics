# E-Commerce Delivery Performance Analytics

Analisis performa pengiriman e-commerce menggunakan dataset publik Olist dari Brasil untuk mengevaluasi ketepatan waktu pengiriman, mengidentifikasi pola keterlambatan, dan menyajikan hasil analisis melalui dashboard interaktif.

**Live Dashboard:** [Delivery Performance Analytics](https://delivery-performance-analytics-chahyo.streamlit.app/)

---

## Project Overview

Proyek ini berfokus pada analisis performa pengiriman pesanan e-commerce menggunakan Olist Brazilian E-Commerce Public Dataset.

Analisis dilakukan untuk memahami ketepatan waktu pengiriman, melihat pola keterlambatan berdasarkan periode dan wilayah pelanggan, serta menyajikan hasilnya melalui dashboard interaktif yang dikembangkan menggunakan Streamlit.

## Objectives

- Mengevaluasi performa pengiriman berdasarkan ketepatan waktu.
- Mengidentifikasi pola keterlambatan pengiriman berdasarkan bulan.
- Membandingkan tingkat keterlambatan berdasarkan wilayah pelanggan.
- Menyajikan hasil analisis dalam bentuk visualisasi interaktif.
- Menghasilkan insight sebagai bahan evaluasi performa pengiriman.

## Dataset

- **Source:** [Olist Brazilian E-Commerce Public Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
- **Domain:** E-commerce and Delivery Performance
- **Data Used:** Informasi pesanan, pelanggan, dan tanggal pengiriman yang relevan untuk analisis.

Dataset Olist terdiri atas beberapa tabel yang saling berhubungan. Data yang relevan digunakan untuk menganalisis waktu pengiriman aktual dan estimasi waktu pengiriman.

## Tools & Technologies

| Tools | Purpose |
|---|---|
| Python | Pengolahan dan analisis data |
| Pandas | Manipulasi dan pembersihan data |
| SQLite | Pengelolaan dan query data |
| Plotly | Visualisasi data interaktif |
| Streamlit | Pengembangan dashboard interaktif |

## Methodology

### 1. Data Preparation

Menyiapkan dan menggabungkan data pesanan, pelanggan, serta informasi tanggal pengiriman yang dibutuhkan untuk analisis.

### 2. Data Cleaning

Memeriksa kelengkapan data tanggal dan menyiapkan data untuk perhitungan waktu pengiriman serta identifikasi keterlambatan.

### 3. Delivery Performance Analysis

Membandingkan tanggal pengiriman aktual dengan estimasi tanggal pengiriman untuk mengidentifikasi pesanan yang terlambat.

### 4. Exploratory Data Analysis

Menganalisis performa pengiriman berdasarkan periode waktu dan wilayah pelanggan untuk mengidentifikasi pola keterlambatan.

### 5. Dashboard Development

Mengembangkan dashboard interaktif menggunakan Streamlit dan Plotly. Dashboard menyediakan filter tanggal dan wilayah untuk membantu pengguna mengeksplorasi hasil analisis.

## Key Insights

Berdasarkan hasil analisis yang tercatat pada dashboard proyek:

| Metric | Result |
|---|---:|
| Pesanan terkirim yang dianalisis | 96.476 |
| Pesanan terlambat | 7.827 |
| Pengiriman tepat waktu | 91,89% |
| Pengiriman terlambat | 8,11% |
| Rata-rata waktu pengiriman | 12,6 hari |

### Additional Findings

- **Periode dengan tingkat keterlambatan tertinggi:** Maret 2018, sebesar 21,36% dari 7.003 pesanan.
- **Wilayah dengan tingkat keterlambatan tertinggi:** Alagoas (AL), sebesar 23,93% dari 397 pesanan.

Hasil analisis dapat berubah sesuai dengan filter tanggal, wilayah, dan cakupan data yang digunakan.

## Recommendations

Berdasarkan pola yang ditemukan, beberapa hal yang dapat menjadi bahan evaluasi adalah:

1. **Evaluasi berdasarkan periode:** meninjau performa pengiriman pada periode dengan tingkat keterlambatan tinggi.
2. **Evaluasi berdasarkan wilayah:** memeriksa kondisi pengiriman di wilayah dengan persentase keterlambatan tinggi.
3. **Pemantauan performa:** menggunakan indikator ketepatan waktu dan keterlambatan untuk memantau perubahan performa pengiriman.
4. **Analisis lanjutan:** mengevaluasi faktor lain yang mungkin berkaitan dengan keterlambatan menggunakan data tambahan yang relevan.

Rekomendasi ini merupakan usulan evaluasi berdasarkan pola analisis dan tidak menyatakan penyebab keterlambatan secara pasti.

## Dashboard

Dashboard interaktif memungkinkan pengguna mengeksplorasi performa pengiriman berdasarkan filter tanggal dan wilayah.

**[Open Live Dashboard](https://delivery-performance-analytics-chahyo.streamlit.app/)**
