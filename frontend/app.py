import streamlit as st
import requests

st.set_page_config(page_title="Agri-LLM Hub", page_icon="🌾")
BACKEND_URL = "http://localhost:8000"

st.title("🌾 Agri-LLM Knowledge Hub")

# Real-time data in Sidebar
st.sidebar.header("📍 Real-time Insights")
state = st.sidebar.selectbox("Select State", ["Haryana", "Punjab", "UP", "Rajasthan"])
commodity = st.sidebar.text_input("Commodity", "Wheat")

if st.sidebar.button("Get Live Updates"):
    params = {"state": state, "commodity": commodity}
    data = requests.get(f"{BACKEND_URL}/market-weather", params=params).json()
    if 'weather' in data and data['weather']:
        st.sidebar.metric("Temp", f"{data['weather']['temperature']}°C")
    st.sidebar.info(f"📊 {data['mandi']}")

tab1, tab2 = st.tabs(["Expert Advisor", "Crop Doctor (Vision)"])

with tab1:
    query = st.text_input("Ask about pesticides or farming:")
    if st.button("Get Advice"):
        res = requests.post(f"{BACKEND_URL}/ask", data={"instruction": query}).json()
        st.success(res['answer'])
        # Voice assistance
        audio_url = f"{BACKEND_URL}/speak?text={res['answer']}"
        st.audio(audio_url)

with tab2:
    img = st.file_uploader("Upload leaf photo", type=["jpg", "png"])
    if img and st.button("Analyze"):
        files = {"file": img.getvalue()}
        res = requests.post(f"{BACKEND_URL}/diagnose", files=files).json()
        st.write(f"**Diagnosis:** {res['diagnosis']}")
        st.warning(f"**Expert Remedy:** {res['advice']}")
        # Voice assistance for diagnosis
        audio_url = f"{BACKEND_URL}/speak?text={res['advice']}"
        st.audio(audio_url)