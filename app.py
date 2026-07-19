import os
# BARIS PENYELAMAT: Harus dipanggil paling awal sebelum TensorFlow!
os.environ['TF_USE_LEGACY_KERAS'] = '1'

import json
import uuid
import numpy as np
from flask import Flask, request, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import preprocess_input

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # Maksimal 5MB
app.secret_key = 'batiklens-secret-key-2026-unibba'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'bmp'}

# Pastikan folder upload ada
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load Model & Label
MODEL_PATH = 'models/batik_vgg16.h5'
LABEL_PATH = 'models/class_indices.json'

model = None
labels = {}

if os.path.exists(MODEL_PATH) and os.path.exists(LABEL_PATH):
    model = load_model(MODEL_PATH)
    with open(LABEL_PATH, 'r') as f:
        labels = json.load(f)
        # Baris yang diperbaiki: menukar posisi v dan k agar value (angka indeks) menjadi key
        labels = {int(v): k for k, v in labels.items()}

# ============================
#  Data Informasi Motif Batik
# ============================
BATIK_INFO = {
    "batik_betawi": {
        "asal": "Jakarta (Betawi)",
        "deskripsi": "Batik Betawi merupakan warisan budaya masyarakat asli Jakarta yang kaya akan motif flora dan fauna lokal. Motifnya terinspirasi dari kehidupan sehari-hari.",
        "keunikan": "Warna cerah dan berani dengan dominasi merah, biru, dan hijau khas pesisir Batavia.",
        "icon": "🦁"
    },
    "batik_bokor_kencono": {
        "asal": "Jawa Tengah",
        "deskripsi": "Motif geometris yang mengambil inspirasi dari bentuk bokor (wadah/tempat) yang terbuat dari emas (kencono).",
        "keunikan": "Melambangkan harapan akan kewibawaan, kesejahteraan, dan kedudukan yang terhormat di masyarakat.",
        "icon": "🏺"
    },
    "batik_buketan": {
        "asal": "Pekalongan, Jawa Tengah",
        "deskripsi": "Terinspirasi dari kata 'bouquet' dalam bahasa Belanda yang berarti rangkaian bunga. Sangat dipengaruhi oleh budaya Eropa.",
        "keunikan": "Menampilkan corak rangkaian bunga atau tumbuhan yang sangat detail, feminin, dan elegan dengan warna-warna cerah.",
        "icon": "💐"
    },
    "batik_dayak": {
        "asal": "Kalimantan",
        "deskripsi": "Motif Dayak terinspirasi dari tato dan ukiran tradisional suku Dayak yang penuh dengan elemen alam dan spiritual.",
        "keunikan": "Pola tribal yang sangat khas, simetris, berani, dan sering kali menggunakan perpaduan warna kontras.",
        "icon": "🛡️"
    },
    "batik_jlamprang": {
        "asal": "Pekalongan, Jawa Tengah",
        "deskripsi": "Motif geometris khas Pekalongan yang sangat dipengaruhi oleh kebudayaan Arab dan India (khususnya kain Patola).",
        "keunikan": "Berbentuk ceplokan (lingkaran/persegi) berulang tanpa putus yang melambangkan hubungan dunia kosmis dengan Sang Pencipta.",
        "icon": "💠"
    },
    "batik_kawung": {
        "asal": "Yogyakarta",
        "deskripsi": "Batik Kawung merupakan salah satu motif batik paling tua dan sakral di Jawa. Berbentuk lingkaran-lingkaran yang menyerupai buah aren.",
        "keunikan": "Motif sakral yang dahulu eksklusif hanya untuk keluarga keraton sebagai simbol pengendalian diri dan hati yang bersih.",
        "icon": "👑"
    },
    "batik_liong": {
        "asal": "Cirebon / Pekalongan",
        "deskripsi": "Liong berarti Naga. Motif ini merupakan hasil akulturasi kuat dari budaya Tionghoa yang dibawa oleh para pedagang pada zaman dahulu.",
        "keunikan": "Menampilkan sosok naga yang dipercaya sebagai simbol kekuatan, kejayaan, keberuntungan, dan kemakmuran.",
        "icon": "🐉"
    },
    "batik_mega_mendung": {
        "asal": "Cirebon, Jawa Barat",
        "deskripsi": "Batik Megamendung adalah ikon batik Cirebon yang paling terkenal. Motifnya menggambarkan awan berlapis yang melambangkan dunia atas.",
        "keunikan": "Motif awan dengan gradasi warna yang sangat khas. Mengajarkan agar manusia bisa meredam amarah saat sedang 'mendung' (emosi).",
        "icon": "☁️"
    },
    "batik_parang": {
        "asal": "Yogyakarta / Solo",
        "deskripsi": "Salah satu motif batik tertua. Berbentuk menyerupai huruf S yang berkesinambungan membentuk garis diagonal.",
        "keunikan": "Melambangkan ombak samudra yang tak pernah berhenti bergerak, dimaknai sebagai semangat juang dan pantang menyerah.",
        "icon": "⚔️"
    },
    "batik_sekarjagad": {
        "asal": "Yogyakarta & Surakarta",
        "deskripsi": "Berasal dari kata 'Sekar' (bunga/keindahan) dan 'Jagad' (dunia). Motif ini menggabungkan berbagai macam corak tradisional menjadi satu kesatuan.",
        "keunikan": "Terlihat seperti peta dunia yang terbagi-bagi, melambangkan keindahan keragaman dan persatuan seluruh dunia.",
        "icon": "🌍"
    },
    "batik_sidoluhur": {
        "asal": "Yogyakarta / Surakarta",
        "deskripsi": "Berakar dari kata 'Sido' (jadi/terlaksana) dan 'Luhur' (mulia). Merupakan batik keraton untuk upacara penting.",
        "keunikan": "Mengandung doa agar pemakainya dapat mencapai kedudukan tinggi dan memiliki budi pekerti yang luhur.",
        "icon": "✨"
    },
    "batik_sidomukti": {
        "asal": "Surakarta (Solo)",
        "deskripsi": "Bermakna 'selalu makmur dan bahagia'. Merupakan batik khas Solo yang paling sering digunakan oleh sepasang pengantin.",
        "keunikan": "Memiliki doa filosofis yang kuat agar pemakainya meraih kebahagiaan abadi dan rezeki yang berkecukupan.",
        "icon": "🌟"
    },
    "batik_sidomulyo": {
        "asal": "Surakarta (Solo)",
        "deskripsi": "Hampir mirip dengan Sidomukti, 'Mulyo' memiliki arti kemuliaan. Menggunakan pola dasar geometris yang terstruktur rapi.",
        "keunikan": "Membawa harapan agar keluarga yang dibina selalu mendapatkan kemuliaan dan dihormati dalam kehidupan sosial.",
        "icon": "💎"
    },
    "batik_singa_barong": {
        "asal": "Cirebon, Jawa Barat",
        "deskripsi": "Motif yang terinspirasi dari Kereta Singa Barong dari Keraton Kasepuhan Cirebon. Merupakan perpaduan luar biasa dari berbagai budaya.",
        "keunikan": "Menggabungkan unsur Singa (Eropa/Hindu), Naga (Tiongkok), Buraq (Islam/Arab), dan Gajah (India).",
        "icon": "🦁"
    },
    "batik_srikaton": {
        "asal": "Surakarta (Solo)",
        "deskripsi": "Motif klasik yang namanya bermakna 'Sri' (indah/agung) dan 'Katon' (terlihat). Biasanya dipenuhi dengan ornamen floral dan burung.",
        "keunikan": "Dirancang untuk memberikan kesan luwes, memancarkan wibawa, dan pesona keindahan bagi siapa saja yang memakainya.",
        "icon": "🌸"
    },
    "batik_tribusono": {
        "asal": "Jawa Tengah",
        "deskripsi": "Kata Tribusono merujuk pada kombinasi tiga elemen gaya atau ornamen. Seringkali menggunakan perpaduan warna sogan klasik.",
        "keunikan": "Menghasilkan kesan tiga dimensi atau tiga kekuatan alam yang menyatu, mencerminkan keseimbangan hidup.",
        "icon": "⚖️"
    },
    "batik_tujuh_rupa": {
        "asal": "Pekalongan, Jawa Tengah",
        "deskripsi": "Dikenal sebagai mahakarya dari pesisir yang menggabungkan percampuran budaya Tiongkok, Arab, dan Jawa.",
        "keunikan": "Sangat kaya akan ragam hias flora dan fauna dengan warna-warni yang sangat dinamis dan ceria.",
        "icon": "🎨"
    },
    "batik_tuntrum": {
        "asal": "Surakarta (Solo)",
        "deskripsi": "Motif Truntum diciptakan oleh Kanjeng Ratu Kencana. Berbentuk seperti taburan bintang-bintang kecil yang bersinar di langit malam.",
        "keunikan": "Melambangkan cinta yang 'tumaruntum' (tumbuh bersemi kembali) tanpa syarat dan abadi. Wajib dipakai oleh orang tua pengantin.",
        "icon": "🌌"
    },
    "batik_wahyu_tumurun": {
        "asal": "Yogyakarta & Surakarta",
        "deskripsi": "Pola yang menonjolkan bentuk mahkota terbang, ayam alas, atau burung, dengan latar belakang yang klasik.",
        "keunikan": "Berisi harapan agung agar pemakainya selalu mendapat berkah, rahmat, dan petunjuk (wahyu) dari Tuhan Yang Maha Esa.",
        "icon": "🕊️"
    },
    "batik_wirasat": {
        "asal": "Surakarta (Solo)",
        "deskripsi": "Wirasat atau firasat adalah motif kompilasi yang menyatukan unsur-unsur dari motif Truntum, Cakar Ayam, Sindur, dan lainnya.",
        "keunikan": "Sarat akan nasihat dan harapan. Dikhususkan bagi orang tua agar dapat memberikan tuntunan yang baik bagi anak-anaknya.",
        "icon": "📜"
    }
}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def model_predict(img_path, model):
    img = image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    preds = model.predict(x)
    class_idx = int(np.argmax(preds, axis=1)[0])
    confidence = float(np.max(preds))
    return labels.get(class_idx, "tidak-dikenali"), confidence


# ============================
#  Routes
# ============================
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html', batik_info=BATIK_INFO)


@app.route('/predict', methods=['POST'])
def upload():
    if 'file' not in request.files:
        flash('Tidak ada file yang dipilih.', 'error')
        return redirect(url_for('index'))

    f = request.files['file']

    if f.filename == '':
        flash('Tidak ada file yang dipilih.', 'error')
        return redirect(url_for('index'))

    if not allowed_file(f.filename):
        flash('Format file tidak didukung. Gunakan PNG, JPG, JPEG, atau WEBP.', 'error')
        return redirect(url_for('index'))

    if model is None:
        flash('Model AI belum dimuat. Pastikan file model tersedia di folder /models.', 'error')
        return redirect(url_for('index'))

    try:
        # Buat nama file unik agar tidak terjadi konflik
        ext = f.filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4().hex}.{ext}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        f.save(filepath)

        # Prediksi
        motif_key, confidence = model_predict(filepath, model)
        
        # Format nama motif untuk ditampilkan (misal: "Batik Mega Mendung")
        motif_name = motif_key.replace('_', ' ').title()
        
        acc_percent = f"{confidence * 100:.2f}%"
        acc_value = round(confidence * 100, 2)

        # Info motif batik
        # Hanya gunakan string asli yang di-lowercase karena key di BATIK_INFO sekarang menggunakan underscore
        normalized_key = motif_key.lower()
        info = BATIK_INFO.get(normalized_key, {})
        is_low_confidence = confidence < 0.60

        return render_template(
            'result.html',
            image_file=unique_filename,
            motif=motif_name,
            motif_key=normalized_key,
            accuracy=acc_percent,
            acc_value=acc_value,
            info=info,
            is_low_confidence=is_low_confidence
        )

    except Exception as e:
        flash(f'Terjadi kesalahan saat memproses gambar: {str(e)}', 'error')
        return redirect(url_for('index'))


# ============================
#  Error Handlers
# ============================
@app.errorhandler(404)
def not_found(e):
    return render_template('error.html', code=404, message="Halaman Tidak Ditemukan"), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('error.html', code=500, message="Kesalahan Internal Server"), 500


@app.errorhandler(413)
def too_large(e):
    flash('Ukuran file terlalu besar. Maksimal 5MB.', 'error')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)