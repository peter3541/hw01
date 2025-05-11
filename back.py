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
    
def add_record(amount, category, note):
    data = load_data()
    record = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "amount": amount,
        "category": category,
        "note": note,
        # "type": "收入" if is_income else "支出"
    }
    data.append(record)
    save_data(data)

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def calculate_total(data):
    total = 0
    for item in data:
        # if item["type"] == "收入":
        total += item["amount"]
        # else:
        #     total -= item["amount"]
    return total

def calculate_category_totals(data):
    """
    計算各分類的總金額。

    Args:
        data (list): 包含記帳資料的清單，每個元素是一個字典，包含 'category' 和 'amount' 等欄位。

    Returns:
        dict: 各分類的總金額。
    """
    totals = {
        "早餐": 0,
        "午餐": 0,
        "晚餐": 0,
        "宵夜": 0,
        "飲料": 0,
        "文具": 0,
        "課本": 0,
        "遊戲": 0,
        "其他": 0,
    }
    
    for item in data:
        if item["category"] in totals:
            totals[item["category"]] += item["amount"]
    
    return totals
    
# def calculate_total(data):
#     total = 0
#     for item in data:
#         if item["category"] == "早餐":
#             if item["type"] == "收入":
#                 total += item["amount"]
#             else:
#                 total -= item["amount"]
#         elif item["category"] == "午餐":
#             if item["type"] == "收入":
#                 total += item["amount"]
#             else:
#                 total -= item["amount"]
#         elif item["category"] == "晚餐":
#             if item["type"] == "收入":
#                 total += item["amount"]
#             else:
#                 total -= item["amount"]
#         elif item["category"] == "宵夜":
#             if item["type"] == "收入":
#                 total += item["amount"]
#             else:
#                 total -= item["amount"]
#         elif item["category"] == "飲料":
#             if item["type"] == "收入":
#                 total += item["amount"]
#             else:
#                 total -= item["amount"]
#         elif item["category"] == "文具":
#             if item["type"] == "收入":
#                 total += item["amount"]
#             else:
#                 total -= item["amount"]
#         elif item["category"] == "課本":
#             if item["type"] == "收入":
#                 total += item["amount"]
#             else:
#                 total -= item["amount"]
#         elif item["category"] == "遊戲":
#             if item["type"] == "收入":
#                 total += item["amount"]
#             else:
#                 total -= item["amount"]
#         elif item["category"] == "其他":
#             if item["type"] == "收入":
#                 total += item["amount"]
#             else:
#                 total -= item["amount"]
#         = f" [{item['category']}]"
#     return total

#     ["早餐", "午餐", "晚餐", "宵夜", "飲料", "文具", "課本", "遊戲", "其他"]