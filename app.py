import streamlit as st
from ultralytics import YOLO
from PIL import Image
import pandas as pd

st.set_page_config(
    page_title="Helmet Safety Detection",
    layout="centered"
)

st.title("Helmet Safety Detection with YOLOv11")
st.markdown("Upload một ảnh và hệ thống sẽ trả về kết quả nhận diện.")

# Load model
@st.cache_resource
def load_model():
    # Đường dẫn tương đối trong repo
    return YOLO("models/helmet_detection_best.pt")

model = load_model()

# Upload image
uploaded_file = st.file_uploader("📷 Upload an image", type=["jpg", "png", "jpeg"])

if uploaded_file:
    img = Image.open(uploaded_file).convert("RGB")
    st.image(img, caption="Ảnh gốc", use_container_width=True)

    # Detection
    results = model(img)

    # Annotated image
    annotated_img = results[0].plot()
    st.image(annotated_img, caption="Kết quả nhận diện", use_container_width=True)

    # Result table
    boxes = results[0].boxes
    if boxes is not None and len(boxes) > 0:
        data = []
        for b in boxes:
            cls = int(b.cls[0])
            conf = float(b.conf[0])
            xyxy = b.xyxy[0].tolist()
            data.append({
                "Class": model.names[cls],
                "Confidence": f"{conf:.2f}",
                "x1": int(xyxy[0]),
                "y1": int(xyxy[1]),
                "x2": int(xyxy[2]),
                "y2": int(xyxy[3])
            })
        df = pd.DataFrame(data)
        st.markdown("### 📊 Chi tiết nhận diện")
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("⚠️ Không phát hiện được vật thể nào.")
