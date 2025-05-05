import json
from datetime import datetime
import os


DATA_FILE = 'data.json'



def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        return []
    
def add_record(amount, category, note, is_income):
    data = load_data()
    record = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "amount": amount,
        "category": category,
        "note": note,
        "type": "收入" if is_income else "支出"
    }
    data.append(record)
    save_data(data)

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    