# BatikLens 🖼️🎨

BatikLens adalah aplikasi web berbasis AI (Kecerdasan Buatan) yang dapat mengenali dan mengklasifikasikan berbagai jenis motif batik secara otomatis. Menggunakan model Deep Learning (VGG16) yang telah dilatih secara khusus untuk mendeteksi berbagai motif batik populer dari seluruh nusantara.

## Fitur ✨

*   **Deteksi Otomatis**: Mengunggah gambar batik, dan AI akan menganalisis motifnya.
*   **Informasi Detail**: Memberikan penjelasan terkait asal daerah, filosofi, dan makna dari motif batik yang diprediksi.
*   **Antarmuka Pengguna**: Desain UI yang indah dan responsif untuk kemudahan penggunaan.
*   **Tingkat Kepercayaan (Confidence Level)**: Memberikan persentase seberapa yakin AI terhadap hasil identifikasinya.

## Teknologi yang Digunakan 💻

*   **Backend**: Flask (Python)
*   **Deep Learning Framework**: TensorFlow / Keras
*   **Model Arsitektur**: VGG16 (Pre-trained Convolutional Neural Network)
*   **Frontend**: HTML, CSS, JavaScript

## Cara Menjalankan Secara Lokal 🚀

1.  **Clone repository ini:**
    ```bash
    git clone https://github.com/USERNAME/BatikLens.git
    cd BatikLens
    ```

2.  **Buat Virtual Environment (Opsional namun disarankan):**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Jalankan aplikasi:**
    ```bash
    python app.py
    ```

5.  **Akses aplikasi:**
    Buka web browser dan akses ke `http://127.0.0.1:5000`

## Struktur Direktori 📁
```
BatikLens/
├── app.py                  # Skrip utama Flask (Backend dan Routing)
├── models/                 # Model AI yang sudah dilatih (.h5) dan class_indices
│   ├── batik_vgg16.h5
│   └── class_indices.json
├── static/                 # Aset statis seperti CSS, gambar, dan folder uploads
│   └── uploads/            # Tempat gambar pengguna sementara diunggah
├── templates/              # File HTML untuk tampilan frontend
│   ├── index.html
│   ├── about.html
│   ├── result.html
│   └── error.html
├── requirements.txt        # Daftar dependency Python
├── Dockerfile              # Konfigurasi Docker untuk deploy ke Hugging Face
└── README.md               # Dokumentasi proyek
```

## Penggunaan Model 🧠
Pastikan file model `batik_vgg16.h5` berukuran sekitar ~117MB ada di dalam folder `models/`. Jika tidak ada, pastikan untuk menggunakan Git LFS ketika mengunduh repo ini.

## Deployment (Hugging Face Spaces) ☁️
Aplikasi ini sudah dipersiapkan untuk bisa dideploy ke [Hugging Face Spaces](https://huggingface.co/spaces) menggunakan Docker. File `Dockerfile` telah disediakan sehingga Hugging Face dapat langsung mem-build dan menjalankan aplikasi Flask ini di cloud.
