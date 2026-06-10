import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import base64

def img_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

logo_padi = img_to_base64("image/padi.avif")

st.set_page_config(
    page_title="RiceVision – Klasifikasi Jenis Beras",
    page_icon="🌾",
    layout="centered",
)

st.markdown("""
<link rel="stylesheet"
href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined" />
            
<style>
@import url('https://fonts.googleapis.com/css2?family=Lora:wght@600;700&family=Inter:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #0F1117;
    color: #FFFFFF;
}

#MainMenu, footer, header {
    visibility: hidden;
}

.block-container {
    padding-top: 2.5rem !important;
    max-width: 680px;
}

.page-header {
    text-align: center;
    margin-bottom: 2.5rem;
}

.page-eyebrow {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #7CFC8A;
    margin-bottom: 0.6rem;
}

.page-title {
    font-family: 'Lora', Georgia, serif;
    font-size: 2.6rem;
    font-weight: 700;
    color: #FFFFFF;
    line-height: 1.15;
    margin: 0 0 0.75rem;
}

.page-title span {
    color: #4ADE80;
}

.page-desc {
    font-size: 0.92rem;
    color: #D1D5DB;
    line-height: 1.65;
    max-width: 480px;
    margin: 0 auto;
}

.rule {
    border: none;
    border-top: 1.5px solid #2D3748;
    margin: 2rem 0;
}

.section-label {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #86EFAC;
    margin-bottom: 0.75rem;
    display: block;
}

/* File uploader */
[data-testid="stFileUploader"] > div {
    background: #1A1F2E;
    border: 2px dashed #4ADE80;
    border-radius: 1rem;
    transition: border-color 0.2s, background 0.2s;
}

[data-testid="stFileUploader"] > div:hover {
    border-color: #86EFAC;
    background: #1F2937;
}

[data-testid="stFileUploaderDropzoneInstructions"] div span {
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    color: #FFFFFF;
}

[data-testid="stFileUploaderDropzoneInstructions"] div small {
    color: #9CA3AF;
}

/* Button */
[data-testid="stBaseButton-primary"] {
    background: #16A34A !important;
    border: none !important;
    border-radius: 0.75rem !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    padding: 0.75rem !important;
}

[data-testid="stBaseButton-primary"]:hover {
    background: #15803D !important;
}

/* Result card */
.result-card {
    background: #1A1F2E;
    border-radius: 1.25rem;
    padding: 1.6rem 1.8rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.35);
    margin-top: 1rem;
}

.result-top-label {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #86EFAC;
    margin-bottom: 0.4rem;
}

.result-species {
    font-family: 'Lora', serif;
    font-size: 2rem;
    font-weight: 700;
    color: #FFFFFF;
    margin: 0 0 1rem;
}

.conf-row {
    display: flex;
    justify-content: space-between;
    font-size: 0.82rem;
    font-weight: 500;
    color: #D1D5DB;
    margin-bottom: 0.4rem;
}

.conf-track {
    background: #374151;
    border-radius: 999px;
    height: 8px;
    overflow: hidden;
}

.conf-fill {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, #16A34A, #86EFAC);
}

.conf-number {
    font-family: 'Lora', serif;
    font-size: 1.5rem;
    font-weight: 600;
    color: #4ADE80;
    margin-top: 0.6rem;
}

.warn-strip {
    background: #1F2937;
    border-left: 3px solid #4ADE80;
    border-radius: 0 0.5rem 0.5rem 0;
    padding: 0.65rem 0.9rem;
    font-size: 0.82rem;
    color: #FFFFFF;
    margin-top: 1rem;
}
            
.material-symbols-outlined {
    font-size: 20px;
    vertical-align: middle;
    margin-right: 6px;
}
</style>
""", unsafe_allow_html=True)


# HEADER
st.markdown(f"""
<div class="page-header">
    <div class="page-eyebrow">Ujian Akhir Semester · Deep Learning</div>
    <div class="page-title">
            <img src="data:image/png;base64,{logo_padi}" style="height:40px; vertical-align:middle; margin-right:6px;">
            Rice<span>Vision</span>
    </div>
    <p class="page-desc">
        Sistem klasifikasi jenis beras berbasis <strong>Convolutional Neural Network (CNN)</strong>.
        Unggah foto butiran beras, lalu klik <em>Prediksi</em> — model akan mengidentifikasi
        jenisnya beserta tingkat kepercayaan prediksi.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<hr class='rule'>", unsafe_allow_html=True)


# UPLOAD
# Pendekatan: pakai st.file_uploader langsung (drag & drop sudah built-in)
# dan percantik tampilannya lewat CSS di atas — tanpa JS custom yang bermasalah.
st.markdown('<span class="section-label">1 · Unggah Gambar Beras</span>', unsafe_allow_html=True)

uploaded = st.file_uploader(
    label="Seret & lepas gambar di sini, atau klik Browse files",
    type=["jpg", "jpeg", "png", "webp"],
)

st.markdown("<hr class='rule'>", unsafe_allow_html=True)


# TOMBOL PREDIKSI
st.markdown('<span class="section-label">2 · Jalankan Prediksi</span>', unsafe_allow_html=True)

predict_clicked = st.button(
    ":material/search: Prediksi Jenis Beras",
    type="primary",
    use_container_width=True,
    disabled=(uploaded is None),
)


# HASIL
if predict_clicked and uploaded:
    st.markdown("<hr class='rule'>", unsafe_allow_html=True)
    st.markdown('<span class="section-label">3 · Hasil Prediksi</span>', unsafe_allow_html=True)

    img = Image.open(uploaded).convert("RGB")
    st.image(img, use_container_width=True, caption=f"📁 {uploaded.name}")

    # TODO: Kirim ke backend 
    # import requests, io
    # buf = io.BytesIO()
    # img.save(buf, format="JPEG")
    # response = requests.post(
    #     "http://localhost:8000/predict",
    #     files={"file": (uploaded.name, buf.getvalue(), "image/jpeg")},
    # )
    # data            = response.json()
    # predicted_label = data["label"]
    # confidence      = data["confidence"]
    #
    # PLACEHOLDER — hapus setelah backend tersambung:
    predicted_label = "Basmati"
    confidence      = 0.923
    #

    conf_pct  = confidence * 100
    warn_html = (
        "<div class='warn-strip'>"
        "<span class='material-symbols-outlined'>warning</span>"
        "<strong>Confidence rendah.</strong>"
        "Gambar mungkin bukan jenis beras yang dikenal, atau kualitas foto kurang jelas.</div>"
        if confidence < 0.50 else ""
    )

    st.markdown(f"""
    <div class="result-card">
        <p class="result-top-label">Jenis Beras Terdeteksi</p>
        <p class="result-species">{predicted_label}</p>
        <div class="conf-row">
            <span>Confidence Score</span>
            <span>{conf_pct:.1f}%</span>
        </div>
        <div class="conf-track">
            <div class="conf-fill" style="width:{conf_pct:.1f}%;"></div>
        </div>
        <p class="conf-number">{conf_pct:.1f}%</p>
        {warn_html}
    </div>
    """, unsafe_allow_html=True)
