# RiceVision

## Deskripsi Proyek

RiceVision adalah aplikasi klasifikasi jenis beras berbasis Deep Learning menggunakan arsitektur Convolutional Neural Network (CNN). Model dilatih menggunakan TensorFlow dan diekspor ke format ONNX agar dapat digunakan secara efisien pada lingkungan inferensi menggunakan ONNX Runtime.

Aplikasi ini dikembangkan oleh:
1. Rezza Ramadhana (2308107010019)
2. Naufal Hanif (2308107010025)

Aplikasi ini terdiri dari dua komponen utama:
1. Backend API menggunakan FastAPI untuk melayani proses inferensi model.
2. Frontend menggunakan Streamlit untuk menyediakan antarmuka pengguna berbasis web.

Model mampu mengklasifikasikan lima jenis beras:
* Arborio
* Basmati
* Ipsala
* Jasmine
* Karacadag

## Teknologi yang Digunakan

* Python 3.x
* TensorFlow
* tf2onnx
* ONNX Runtime
* FastAPI
* Uvicorn
* Streamlit
* Pillow
* NumPy

## Persiapan Lingkungan

### Membuat Virtual Environment

```bash
python -m venv <nama_virtual_env>
```

atau menggunakan `uv`

```bash
uv venv
```

### Mengaktifkan Virtual Environment

```bash
source <nama_virtual_env>/bin/activate
```

### Menginstal Dependensi

```bash
pip install -r requirements.txt
```

atau menggunakan `uv`

```bash
uv add -r requirements.txt
```

### Menjalankan Backend API

Backend API menggunakan FastAPI dan ONNX Runtime untuk melakukan prediksi.

Jalankan perintah berikut:

```bash
uvicorn server.main:app --reload
```

atau menggunakan helper `run.sh`

```bash
./run.sh server
```

Secara default API akan tersedia pada:

```bash
http://localhost:8000
```

Dokumentasi API dapat diakses melalui:

```bash
http://localhost:8000/docs
```

### Menjalankan Frontend Streamlit

Untuk menjalankan antarmuka pengguna:

```bash
streamlit run app/app.py
```

atau menggunakan helper `run.sh`

```bash
./run.sh app
```

Secara default aplikasi akan tersedia pada:

```bash
http://localhost:8501
```
