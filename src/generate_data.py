import os
import glob
import json
import time
import re
import hashlib
from groq import Groq
from tqdm import tqdm
from dotenv import load_dotenv
import PyPDF2

# 1. INITIAL SETUP
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Configuration optimized for 1500+ pages
MODEL_ID = "llama-3.1-8b-instant"
DATA_DIR = "data"
OUTPUT_FILE = os.path.join(DATA_DIR, "agri_train_data.jsonl")

# 2. UTILITY FUNCTIONS
def clean_text(text):
    """Removes non-printable characters and standardizes text for JSON stability."""
    text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text)
    return text.replace('"', "'").replace("\\", "/")

def extract_text_from_pdf(pdf_path):
    """Extracts text from massive PDFs page-by-page to avoid memory spikes."""
    text = ""
    try:
        with open(pdf_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
    except Exception as e:
        print(f"\n[Error] Failed to read {pdf_path}: {e}")
    return clean_text(text)

def get_processed_hashes():
    """Reads the existing JSONL to resume progress and avoid double-spending tokens."""
    processed = set()
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    data = json.loads(line)
                    if "chunk_hash" in data:
                        processed.add(data["chunk_hash"])
                except:
                    continue
    return processed

def generate_qa_pairs(context, filename):
    """Uses Groq API with Auto-Retry logic for Rate Limits."""
    # Use double curly braces {{ }} to escape JSON characters in f-strings
    prompt = f"""
    You are an expert agronomist. Based on the CONTEXT below, generate 3 high-quality 
    Instruction-Response pairs for fine-tuning an LLM.
    
    Format the output strictly as a JSON object with a key "qa_pairs" containing a list:
    {{
      "qa_pairs": [
        {{"instruction": "user question", "response": "expert answer"}}
      ]
    }}

    CONTEXT (Source: {filename}):
    {context[:2500]}
    """
    
    for attempt in range(5):  # Retry up to 5 times for Rate Limits (Error 429)
        try:
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=MODEL_ID,
                response_format={"type": "json_object"}
            )
            data = json.loads(response.choices[0].message.content)
            return data.get("qa_pairs", [])
        except Exception as e:
            if "429" in str(e):
                wait_time = (attempt + 1) * 60  # Wait 1 min, then 2, etc.
                print(f"\n[Rate Limit] Daily quota hit or RPM exceeded. Waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                print(f"\n[API Error] {e}")
                break
    return []

# 3. MAIN PIPELINE
def main():
    pdf_files = glob.glob(os.path.join(DATA_DIR, "*.pdf"))
    processed_hashes = get_processed_hashes()
    
    print(f"🚀 Found {len(pdf_files)} PDFs. {len(processed_hashes)} chunks already completed.")

    for pdf_file in pdf_files:
        filename = os.path.basename(pdf_file)
        full_text = extract_text_from_pdf(pdf_file)
        if not full_text:
            continue

        # --- CHUNKING STRATEGY ---
        # 2000 char context window with a 3500 char step.
        # This scans the whole PDF but skips redundant 'filler' text to save tokens.
        chunks = [full_text[i:i+2000] for i in range(0, len(full_text), 3500)]
        
        for chunk in tqdm(chunks, desc=f"Processing {filename[:20]}"):
            # Generate a unique ID for this specific block of text
            chunk_hash = hashlib.md5(chunk.encode()).hexdigest()
            
            # RESUME LOGIC: Skip if we already have this in our JSONL
            if chunk_hash in processed_hashes:
                continue

            qa_list = generate_qa_pairs(chunk, filename)
            
            if qa_list:
                # Append immediately so we don't lose data on crash
                with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
                    for entry in qa_list:
                        entry["chunk_hash"] = chunk_hash
                        entry["source"] = filename
                        f.write(json.dumps(entry) + "\n")
                processed_hashes.add(chunk_hash)
            
            # Standard delay to stay under Groq's Requests Per Minute (RPM)
            time.sleep(1.2)

    print(f"\n✅ Pipeline Finished! Final dataset: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()