import requests
import io
import streamlit as st
from PIL import Image

BASE_URL = "http://localhost:8000/predict"

def load_css(path: str) -> None:
    with open(path, encoding = "utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

def render_html(path: str, **kwargs) -> None:
    with open(path, encoding = "utf-8") as f:
        st.markdown(f.read().format(**kwargs), unsafe_allow_html = True)

st.set_page_config(
    page_title = "RiceVision – Klasifikasi Jenis Beras",
    page_icon = "🌾",
    layout = "centered",
)

load_css("app/style.css")
render_html("app/header.html")

st.markdown("<hr class='rule'>", unsafe_allow_html = True)
st.markdown("<span class='section-label'>1 · Unggah Gambar Beras</span>", unsafe_allow_html = True)

uploaded = st.file_uploader("Seret & lepas gambar di sini", type = ["jpg", "jpeg", "png", "webp"])

st.markdown("<hr class='rule'>", unsafe_allow_html = True)
st.markdown("<span class='section-label'>2 · Jalankan Prediksi</span>", unsafe_allow_html = True)

predict_clicked = st.button(
    ":material/search: Prediksi Jenis Beras",
    type = "primary",
    use_container_width = True,
    disabled = (uploaded is None)
)

if predict_clicked and uploaded:
    st.markdown("<hr class='rule'>", unsafe_allow_html = True)
    st.markdown("<span class='section-label'>3 · Hasil Prediksi</span>", unsafe_allow_html = True)

    _, col2, _ = st.columns([1, 2, 1])
    image = Image.open(uploaded)
    
    with col2:
        st.image(image, caption = uploaded.name)

    buffer = io.BytesIO()
    image.save(buffer, format = "JPEG")
    
    response = requests.post(
        BASE_URL,
        files = {"file": (uploaded.name, buffer.getvalue(), "image/jpeg")},
    )
    data = response.json()
    
    predicted_label = data["label"]
    confidence = data["confidence"]

    render_html(
        "app/result_card.html",
        label = predicted_label,
        confidence = confidence,
        warning = "<div class='warn-strip'>Confidence rendah</div>" if confidence < 50 else ""
    )