# E-Commerce Delivery Performance Analytics

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)
![Pandas](https://img.shields.io/badge/Pandas-2.0-150458?logo=pandas)
![SQL](https://img.shields.io/badge/SQL-MySQL-orange)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit)

Analisis performa pengiriman e-commerce menggunakan dataset publik Olist dari Brasil untuk mengevaluasi ketepatan waktu pengiriman, mengidentifikasi pola keterlambatan, dan menyajikan hasil analisis melalui dashboard interaktif.

**Dashboard Interaktif:** [Lihat Dashboard](https://cahyokml-delivery-analytics.streamlit.app/)

---

## Project Overview

Proyek ini berfokus pada analisis performa pengiriman pesanan e-commerce menggunakan **Olist Brazilian E-Commerce Public Dataset**.

Analisis dilakukan untuk mengevaluasi ketepatan waktu pengiriman, mengidentifikasi pola keterlambatan berdasarkan periode dan wilayah pelanggan, serta menyajikan hasil analisis melalui dashboard interaktif yang dikembangkan menggunakan Streamlit.

## Objectives

- Mengevaluasi performa pengiriman berdasarkan ketepatan waktu.
- Mengukur persentase pesanan yang mengalami keterlambatan.
- Mengidentifikasi pola keterlambatan pengiriman berdasarkan bulan.
- Membandingkan tingkat keterlambatan berdasarkan wilayah pelanggan.
- Menyajikan hasil analisis dalam bentuk visualisasi interaktif.
- Menghasilkan insight sebagai bahan evaluasi performa pengiriman.

## Dataset

- **Sumber:** [Olist Brazilian E-Commerce Public Dataset ΓÇö Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
- **Domain:** E-commerce dan performa pengiriman.
- **Data yang digunakan:** Informasi pesanan, lokasi pelanggan, tanggal pengiriman aktual, dan estimasi tanggal pengiriman yang relevan untuk analisis.

Dataset Olist terdiri dari beberapa tabel yang saling berhubungan. Data yang relevan digunakan untuk membandingkan tanggal pengiriman aktual dengan estimasi tanggal pengiriman serta menganalisis pola keterlambatan berdasarkan periode dan wilayah.

## Tools & Technologies

| Teknologi    | Kegunaan                                               |
| ------------ | ------------------------------------------------------ |
| Python       | Pengolahan dan analisis data                           |
| Pandas       | Pembersihan, manipulasi, dan transformasi data         |
| SQLite / SQL | Pengelolaan dan query data, sesuai implementasi proyek |
| Plotly       | Pembuatan visualisasi data interaktif                  |
| Streamlit    | Pengembangan dashboard interaktif                      |

## Methodology

### 1. Data Preparation

Menyiapkan dan menggabungkan data pesanan, pelanggan, serta informasi tanggal pengiriman yang diperlukan untuk analisis.

### 2. Data Cleaning

Memeriksa kelengkapan data tanggal dan menyiapkan data yang relevan untuk perhitungan waktu pengiriman serta identifikasi keterlambatan.

### 3. Delivery Performance Analysis

Membandingkan tanggal pengiriman aktual dengan estimasi tanggal pengiriman untuk mengidentifikasi pesanan yang terlambat dan mengevaluasi tingkat ketepatan waktu pengiriman.

### 4. Exploratory Data Analysis

Menganalisis performa pengiriman berdasarkan periode waktu dan wilayah pelanggan untuk mengidentifikasi pola serta perbedaan tingkat keterlambatan.

### 5. Dashboard Development

Mengembangkan dashboard interaktif menggunakan Streamlit dan Plotly. Dashboard menyediakan filter tanggal dan wilayah agar pengguna dapat mengeksplorasi hasil analisis sesuai pilihan yang tersedia.

## Key Insights

Berdasarkan hasil analisis yang sebelumnya tercatat dalam proyek, diperoleh ringkasan berikut:

| Metrik                           |     Hasil |
| -------------------------------- | --------: |
| Pesanan terkirim yang dianalisis |    96.476 |
| Pesanan terlambat                |     7.827 |
| Tingkat pengiriman tepat waktu   |    91,89% |
| Tingkat pengiriman terlambat     |     8,11% |
| Rata-rata waktu pengiriman       | 12,6 hari |

### Temuan Tambahan

- **Periode dengan tingkat keterlambatan tertinggi:** Maret 2018, sebesar 21,36% dari 7.003 pesanan.
- **Wilayah dengan tingkat keterlambatan tertinggi:** Alagoas (AL), sebesar 23,93% dari 397 pesanan.

Hasil analisis dapat berubah sesuai dengan filter tanggal, wilayah, dan cakupan data yang digunakan pada dashboard.

## Recommendations

Berdasarkan pola yang ditemukan, beberapa hal berikut dapat dipertimbangkan sebagai bahan evaluasi:

1. **Evaluasi berdasarkan periode:** Meninjau performa pengiriman pada periode dengan tingkat keterlambatan tinggi untuk memahami pola yang terjadi.
2. **Evaluasi berdasarkan wilayah:** Memeriksa performa pengiriman di wilayah dengan persentase keterlambatan tinggi untuk menentukan kebutuhan analisis lebih lanjut.
3. **Pemantauan performa:** Menggunakan indikator ketepatan waktu dan tingkat keterlambatan untuk memantau perubahan performa pengiriman.
4. **Analisis lanjutan:** Menggabungkan informasi tambahan yang relevan untuk menyelidiki faktor-faktor yang mungkin berkaitan dengan keterlambatan.

Rekomendasi ini merupakan usulan evaluasi berdasarkan hasil analisis, bukan kesimpulan mengenai penyebab keterlambatan yang telah terbukti.

## Dashboard

Dashboard interaktif memungkinkan pengguna mengeksplorasi performa pengiriman berdasarkan filter tanggal dan wilayah yang tersedia.

**[Buka Dashboard Delivery Performance Analytics](https://cahyokml-delivery-analytics.streamlit.app/)**

## Menjalankan Proyek Secara Lokal

### Prasyarat

- Python terpasang pada komputer.
- Git terpasang pada komputer.

### 1. Clone Repositori

```bash
git clone https://github.com/cahyokml/Delivery-Performance-Analytics.git
cd Delivery-Performance-Analytics
```

### 2. Membuat Virtual Environment

```bash
python -m venv .venv
```

Aktifkan virtual environment pada Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Menginstal Dependensi

```bash
pip install -r requirements.txt
```

### 4. Menjalankan Dashboard

Jika file utama aplikasi bernama `app.py`, jalankan perintah berikut:

```bash
streamlit run app.py
```

Pastikan file dataset yang diperlukan tersedia di lokasi yang sesuai dengan konfigurasi aplikasi.

## Kesimpulan

Proyek ini menerapkan analisis data dan visualisasi interaktif untuk mengevaluasi performa pengiriman e-commerce menggunakan dataset publik Olist.

Melalui analisis ketepatan waktu, pola keterlambatan berdasarkan periode, dan perbandingan antarwilayah, proyek ini menyajikan gambaran performa pengiriman serta mengidentifikasi area yang dapat ditinjau lebih lanjut berdasarkan data.

---
