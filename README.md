# 🌾 Agri-LLM Knowledge Hub

Agri-LLM Knowledge Hub is a comprehensive, multimodal AI platform designed to empower farmers and agricultural experts with real-time insights, crop diagnosis, and expert advice. Built on top of a fine-tuned **Llama 3.1 8B** model, the hub integrates vision, voice, and live data to provide a seamless agricultural assistant.

## 🚀 Key Features

- **Fine-Tuned Llama 3.1 8B**: Expert advice on agriculture using a specialized dataset trained with **Unsloth** and **QLoRA**.
- **Multimodal Crop Diagnosis**: Integrated vision pipeline (BLIP) for identifying crop diseases from uploaded leaf images.
- **Voice Assistance (TTS)**: Integrated Text-to-Speech (gTTS) for hands-free audio advice, making information more accessible.
- **Real-Time Data Integration**: 
  - **Live Weather**: Powered by Open-Meteo for precise local forecasts.
  - **Market Prices**: Live Mandi data fetched from **Agmarknet** (OGD India) based on state and commodity.
- **Asynchronous Backend**: High-performance **FastAPI** server ensuring smooth model inference and API handling.
- **Interactive UI**: User-friendly **Streamlit** dashboard for easy access to all features.

## 📂 Project Structure

```text
├── assets/             # Agricultural datasets and documentation
├── backend/            # FastAPI server and core services
│   ├── main.py         # Main API endpoints (LLM, Vision, TTS)
│   └── services.py     # External API integrations (Mandi Prices)
├── frontend/           # Streamlit application
│   └── app.py          # Dashboard UI
├── notebooks/          # Fine-tuning and experimentation notebooks
├── src/                # Data cleaning and generation scripts
├── requirements.txt    # Project dependencies
└── run_all.sh          # Script to launch backend and frontend
```

## 🛠️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/shubhammmgithub/Agri-LLM-Knowledge-Hub.git
cd Agri-LLM-Knowledge-Hub
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configuration
Create a `.env` file in the root directory or set your Agmarknet API key in `backend/services.py`:
```bash
GOV_API_KEY=your_api_key_here
```

## 🚦 Running the Application

Use the provided shell script to start both the backend and frontend simultaneously:

```bash
bash run_all.sh
```

Alternatively, run them separately:
- **Backend**: `uvicorn backend.main:app --reload`
- **Frontend**: `streamlit run frontend/app.py`

## 🧠 Model & Dataset Information

- **Fine-Tuned Model**: The core model is **Llama 3.1 8B**, fine-tuned for agricultural extension and crop management. It includes custom behavioral logic (EOS_TOKEN fixes) to ensure precise and helpful responses.
  - 🚀 **Hugging Face Model**: [Agri-LLM-Llama-3.1-8B](https://huggingface.co/shubhammmx/Agri-LLM-Llama-3.1-8B)
- **Custom Dataset**: The model was trained on a specialized agricultural dataset created from scratch, covering various aspects of farming, pest management, and crop diagnosis.
  - 📊 **Hugging Face Dataset**: [Agri-LLM-Dataset](https://huggingface.co/datasets/shubhammmx/Agri-LLM-Dataset)

## 📄 License

This project is licensed under the MIT License.

---
Built with ❤️ for the Agricultural Community.
