# 🚲 Analisis Data Bike Sharing

Proyek analisis data penyewaan sepeda menggunakan dataset Bike Sharing dari Capital Bikeshare System di Washington DC.

## 📊 Dashboard Streamlit

Dashboard interaktif yang menampilkan:
- Tren dan pola penyewaan sepeda
- Analisis berdasarkan musim dan cuaca
- Perbandingan hari kerja vs akhir pekan
- Pola penyewaan per jam
- Performa bulanan dan tahunan

## 🔍 Insight Utama

### Musiman & Cuaca
- Musim panas dan gugur memiliki rata-rata penyewaan tertinggi
- Temperatur optimal untuk penyewaan adalah 20-25°C
- Cuaca hujan menurunkan penyewaan hingga 30%

### Pola Harian
- Puncak penyewaan pada jam commuting (8 pagi dan 5 sore) di hari kerja
- Akhir pekan menunjukkan distribusi yang lebih merata
- Penggunaan terendah terjadi antara jam 2-4 pagi

### Tren Tahunan
- Peningkatan konsisten dari 2011 ke 2012
- Juni-September adalah bulan dengan performa tertinggi
- Tren musiman yang jelas terlihat

## 🛠️ Teknologi yang Digunakan
- Python
- Streamlit
- Pandas
- Plotly
- Statsmodels

## 🚀 Cara Menjalankan
1. Install requirements: 
   
   `pip install -r requirements.txt`
2. Jalankan dashboard: 
   
   `streamlit run dashboard.py`

## 📝 Dataset
Dataset berisi informasi penyewaan sepeda per jam dan harian selama 2011-2012, termasuk:
- Informasi cuaca (temperatur, kelembaban, kecepatan angin)
- Tipe hari (kerja/libur)
- Musim
- Jumlah penyewaan

## 👨‍💻 Dibuat Oleh
Rizqulloh Rifqi Edwanto

## 📄 Lisensi
Copyright (c) 2024 Rizqulloh Rifqi Edwanto

Izin diberikan secara gratis untuk menggunakan, menyalin, memodifikasi, mendistribusikan, dan menjual perangkat lunak ini (“Perangkat Lunak”) beserta dokumentasinya, dengan syarat:

Pemberitahuan hak cipta dan izin ini harus disertakan dalam setiap salinan.

PERANGKAT LUNAK INI DISEDIAKAN "SEBAGAIMANA ADANYA" TANPA JAMINAN APA PUN. PENULIS ATAU PEMEGANG HAK CIPTA TIDAK BERTANGGUNG JAWAB ATAS KLAIM ATAU KERUGIAN YANG TIMBUL DARI PENGGUNAAN PERANGKAT LUNAK INI.

## 📚 Referensi

- Fanaee-T, H., & Gama, J. (2013). Event Labeling Combining Ensemble Detectors and Background Knowledge. Progress in Artificial Intelligence, 1-15. DOI: 10.1007/s13748-013-0040-3

Dataset sepeda yang digunakan dalam proyek ini berasal dari penelitian di atas yang menganalisis data penyewaan sepeda dari Capital Bikeshare System di Washington DC. Dataset ini telah menjadi referensi penting dalam analisis data time series dan prediksi permintaan layanan berbagi sepeda.

Penelitian tersebut menggabungkan teknik deteksi peristiwa dan pengetahuan latar belakang untuk mengidentifikasi dan melabeli peristiwa-peristiwa penting yang mempengaruhi pola penyewaan sepeda. Metodologi yang digunakan memberikan wawasan berharga tentang bagaimana faktor eksternal seperti cuaca, hari libur, dan acara khusus dapat mempengaruhi perilaku pengguna sistem berbagi sepeda.

