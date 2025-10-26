import streamlit as st
from api_handler.photo_blur import blur_photo
import os
from PIL import Image

# ────── Page Config ──────
st.set_page_config(page_title="Hide my number plate", page_icon="🎥", layout="wide")

# ────── Sticky Header ──────
st.markdown("""
    <style>
        .sticky-header {
            position: sticky;
            top: 0;
            background-color: #0e1117;
            padding: 1rem 0.5rem;
            z-index: 999;
            border-bottom: 1px solid #333;
        }
        .sticky-header h1 {
            font-size: 1.8rem;
            margin: 0;
            color: #FAFAFA;
        }
    </style>
    <div class="sticky-header">
        <h1>🎥 Hide my number plate</h1>
    </div>
""", unsafe_allow_html=True)


st.markdown("Upload a **photo file** to blurr the number plate")

file = st.file_uploader("📤 Upload a photo file", type=["jpeg", "jpg", "png", "JPG"], label_visibility="visible")

models = ["small", "medium"]

# Dropdown with default selection
selected_model = st.selectbox("Choose a model:", models, index=0)
if selected_model == 'small':
    model = r"model/small.pt"
else:
    model = r"model/medium.pt"    

if file:
    file_bytes = file.read()
    file_name = file.name

    MAX_SIZE_MB = 50
    if len(file_bytes) > MAX_SIZE_MB * 1024 * 1024:
        st.error(f"❌ File size exceeds {MAX_SIZE_MB}MB limit. Please upload a smaller video.")
        st.stop()

    photoPath = os.path.join("test_data", file_name)
    os.makedirs("test_data", exist_ok=True)
    os.makedirs("final_data", exist_ok=True)
    with open(photoPath, "wb") as buffer:
        buffer.write(file_bytes)

    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("🎞️ Photo Preview")
        st.image(photoPath)

    with col2:
        st.subheader("🔬 Result")
        st.markdown("*This may take ~10 seconds depending on photo length.*")
        with st.spinner("Blurring Photo..."):
            result = blur_photo(photoPath, file_name, model)
            st.image(result)

