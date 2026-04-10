import json
import random
import os

# Configuration
INPUT_FILE = "data/agri_train_data.jsonl"
TRAIN_FILE = "data/train.jsonl"
VAL_FILE = "data/val.jsonl"

# Junk keywords to filter out meta-talk or document boilerplate
JUNK_KEYWORDS = [
    "this document", "this manual", "appendix", "disclaimer", 
    "views of the authors", "epa", "table of content", "page number"
]

def clean_and_split():
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} not found!")
        return

    raw_data = []
    malformed_lines = 0
    
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            if not line.strip(): # Skip empty lines
                continue
            try:
                data = json.loads(line)
                # Check if the required keys exist
                if "instruction" in data and "response" in data:
                    raw_data.append(data)
                else:
                    malformed_lines += 1
            except json.JSONDecodeError:
                malformed_lines += 1

    print(f"📊 Total lines read: {line_num}")
    print(f"✅ Valid pairs found: {len(raw_data)}")
    print(f"⚠️ Malformed/Empty lines skipped: {malformed_lines}")

    # 1. Deduplication (based on instruction text)
    unique_data = {}
    for entry in raw_data:
        instr = entry["instruction"].strip().lower()
        if instr not in unique_data:
            unique_data[instr] = entry
    
    clean_list = list(unique_data.values())
    print(f"✂️ After deduplication: {len(clean_list)}")

    # 2. Heuristic Filtering
    final_data = []
    for entry in clean_list:
        instr = entry["instruction"].lower()
        resp = entry["response"].lower()
        
        if any(keyword in instr or keyword in resp for keyword in JUNK_KEYWORDS):
            continue
        
        if len(entry["response"]) < 10:
            continue
            
        final_data.append(entry)

    print(f"🧹 After cleaning junk: {len(final_data)}")

    # 3. Shuffle and Split
    random.seed(42)
    random.shuffle(final_data)
    
    split_index = int(len(final_data) * 0.9)
    train_set = final_data[:split_index]
    val_set = final_data[split_index:]

    # 4. Save to files (only keep instruction/response for training)
    with open(TRAIN_FILE, "w", encoding="utf-8") as f:
        for entry in train_set:
            f.write(json.dumps({"instruction": entry["instruction"], "response": entry["response"]}) + "\n")
            
    with open(VAL_FILE, "w", encoding="utf-8") as f:
        for entry in val_set:
            f.write(json.dumps({"instruction": entry["instruction"], "response": entry["response"]}) + "\n")

    print(f"📦 Final Training Set: {len(train_set)} pairs")
    print(f"📦 Final Validation Set: {len(val_set)} pairs")

if __name__ == "__main__":
    clean_and_split()