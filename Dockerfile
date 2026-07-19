FROM python:3.11-slim

# Mengatur direktori kerja di dalam container
WORKDIR /app

# Menyalin file requirements dan menginstalnya
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Menyalin seluruh kode proyek
COPY . .

# Hugging Face Spaces mewajibkan port 7860
EXPOSE 7860

# Menjalankan aplikasi Flask menggunakan Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:7860", "app:app"]