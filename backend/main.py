from fastapi import FastAPI, UploadFile, File, Form
from unsloth import FastLanguageModel
from transformers import pipeline
from gtts import gTTS
import io
from PIL import Image
from fastapi.responses import StreamingResponse
import httpx
from services import get_mandi_prices

app = FastAPI(title="Agri-LLM API")

# Load Fine-tuned model
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "shubhammmx/Agri-LLM-Llama-3.1-8B",
    load_in_4bit = True,
)
FastLanguageModel.for_inference(model)

# Multimodal: Vision pre-processor
vision_model = pipeline("image-to-text", model="Salesforce/blip-image-captioning-base")

@app.post("/ask")
async def ask_expert(instruction: str = Form(...)):
    prompt = f"### Instruction:\n{instruction}\n\n### Response:\n"
    inputs = tokenizer([prompt], return_tensors="pt").to("cuda")
    outputs = model.generate(**inputs, max_new_tokens=128, eos_token_id=tokenizer.eos_token_id)
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True).split("### Response:")[-1].strip()
    return {"answer": answer}

@app.get("/speak")
async def speak(text: str):
    tts = gTTS(text=text, lang='en')
    audio_io = io.BytesIO()
    tts.write_to_fp(audio_io)
    audio_io.seek(0)
    return StreamingResponse(audio_io, media_type="audio/mpeg")

@app.post("/diagnose")
async def diagnose(file: UploadFile = File(...)):
    img_content = await file.read()
    image = Image.open(io.BytesIO(img_content))
    caption = vision_model(image)[0]['generated_text']
    advice_res = await ask_expert(instruction=f"The image of the crop shows: {caption}. What is the expert remedy?")
    return {"diagnosis": caption, "advice": advice_res["answer"]}

@app.get("/market-weather")
async def get_realtime_data(state: str = "Haryana", commodity: str = "Wheat"):
    async with httpx.AsyncClient() as client:
        # Free Open-Meteo Weather API
        w_resp = await client.get("https://api.open-meteo.com/v1/forecast?latitude=28.4&longitude=77.5&current_weather=true")
        weather = w_resp.json().get("current_weather")
        
        # Agmarknet / Mandi Prices
        price = await get_mandi_prices(commodity, state)
        
        return {
            "weather": weather, 
            "mandi": f"{commodity} in {state}: ₹{price}/q" if price != "No data found" else f"{commodity} prices unavailable"
        }