


import streamlit as st
import time
from back import load_data, save_data, add_record, calculate_total,calculate_category_totals,add_budget,balance,budget_load_data,budget_save_data
from datetime import datetime

def delete_record(index):
    data = load_data()
    
    removed = data.pop(index)
    save_data(data)
    st.success(f"已刪除：{removed['date']} {removed['category']} {removed['amount']} 元")
    time.sleep(1)

def budget_delete_record(index):
    data = budget_load_data()
    
    removed = data.pop(index)
    budget_save_data(data)
    st.success(f"已刪除：{removed['budget_month']} {removed['budget_amount']} 元")
    time.sleep(1)

        

st.set_page_config(page_title="簡易記帳小幫手", layout="centered")

with open("style.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# 初始化狀態
if "page" not in st.session_state:
    st.session_state.page = "home"
if "form_saved" not in st.session_state:
    st.session_state.form_saved = False
# if "saved_time" not in st.session_state:
#     st.session_state.saved_time = 0

# 側邊欄按鈕
if st.sidebar.button("首頁"):
    st.session_state.page = "home"
if st.sidebar.button("新增紀錄"):
    st.session_state.page = "add"
if st.sidebar.button("查看紀錄"):
    st.session_state.page = "achieve"
if st.sidebar.button("統計資料"):
    st.session_state.page = "count"
if st.sidebar.button("本月預算"):
    st.session_state.page = "budget"
if st.sidebar.button("本月結算"):
    st.session_state.page = "balance"

# 顯示頁面內容

if st.session_state.page == "home":
    st.markdown("<h1 style='font-size: 50px;'>簡易記帳小幫手</h1>", unsafe_allow_html=True)


if st.session_state.page == "add":
    st.title("新增收支紀錄")

    with st.form("entry_form"):
        amount = st.number_input("金額", min_value=1, step=1)
        category = st.selectbox("分類", ["早餐", "午餐", "晚餐", "宵夜", "飲料", "文具", "課本", "遊戲", "其他"])
        note = st.text_input("備註")
        # is_income = st.radio("收入 / 支出", ["支出", "收入"]) == "收入"
        month=datetime.now().month
        submitted = st.form_submit_button("儲存紀錄")
        if submitted:
            st.session_state.form_saved = True
            add_record(amount, category, note,month)
            

    if st.session_state.form_saved:
            st.success("儲存成功！")
            st.session_state.form_saved = False
            time.sleep(2)
            st.session_state.page = "add"
            st.rerun()

elif st.session_state.page == "achieve":
    st.title("所有記帳紀錄")
    data = load_data()

    if not data:
        st.info("目前沒有任何記錄。")
    else:
        # 按日期降序排序資料
        from datetime import datetime
        sorted_data = sorted(enumerate(data), key=lambda x: datetime.strptime(x[1]["date"], "%Y-%m-%d"), reverse=True)

        # 分組資料，並記錄原始索引
        grouped_data = {}
        for original_index, item in sorted_data:
            date = item["date"]
            if date not in grouped_data:
                grouped_data[date] = []
            grouped_data[date].append((original_index, item))  # 保存原始索引和記錄

        # 顯示分組後的資料
        for date, records in grouped_data.items():
            st.subheader(f"📅 {date}")  # 顯示日期
            for i, (original_index, record) in enumerate(records):
                col1, col2 = st.columns([6, 1])
                with col1:
                    st.write(f" - {record['category']} | {record['amount']} 元 - {record['note']}")
                with col2:
                    if st.button("🗑️ 刪除", key=f"del_{date}_{original_index}"):
                        # 使用原始索引刪除
                        delete_record(original_index)
                        st.rerun()

# elif st.session_state.page == "achieve":
#     # st.markdown("<h1 style='font-size: 50px;'>簡易記帳小幫手</h1>", unsafe_allow_html=True)
#     data = load_data()
    
#     # col3, col4 = st.columns([5, 1])
#     # with col3:
#     #     st.title("所有記帳紀錄")
#     # with col4:    
#     #     categories = ["全部"] + list(set(item["category"] for item in data))
#     #     selected_category = st.selectbox("選擇分類", categories)
#     # if not data:
#     #     st.info("目前沒有任何記錄。")
#     #     filtered_data = []

#     # else:
        
#     #     if selected_category != "全部":
#     #         filtered_data = [item for item in data if item["category"] == selected_category]
#     #     else:
#     #         filtered_data = data
        
#     # for i, item in enumerate(filtered_data):
#     col1, col2 = st.columns([6, 1])
        
#     with col1: 
#             grouped_data = {}
#             for item in data:
#                 date = item["date"]
#                 if data not in grouped_data:
#                     grouped_data[data] = []
#                 grouped_data[data].append(item)

#             # 顯示分組後的資料
#             for date, records in grouped_data.items():
#                 st.subheader(f"📅 {date}")  # 顯示日期
#                 for record in records:
#                     st.write(f" - {record['category']} | {record['amount']} 元 - {record['note']}")
            
#             # st.write(f" [{item['date']}] | {item['category']} | {item['amount']} 元 - {item['note']}")
#     with col2:
#             if st.button("🗑️ 刪除", key=f"del_{i}"):
#                 # delete_record(i)
#                 st.rerun()

    # total=calculate_total(data)
    # st.metric("花費總額", f"${total}")
    



elif st.session_state.page == "count":
    # st.title("支出紀錄")
    # st.subheader("各類別統計")
    st.title("各類別統計")
    data = load_data()
    totals = calculate_category_totals(data)

    # 顯示結果
    for category, total in totals.items():
        st.write(f"{category}：${total}")
    
elif st.session_state.page == "budget":
    st.title("新增預算")
    
    with st.form("entry_form"):
        budget_amount = st.number_input("金額", min_value=1, step=1)
        budget_month = st.selectbox("月份", ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"],index=datetime.now().month - 1)
        # is_income = st.radio("收入 / 支出", ["支出", "收入"]) == "收入"
        
        submitted = st.form_submit_button("儲存紀錄")

        if submitted:
            st.session_state.form_saved = True
            add_budget(budget_amount, budget_month)

    if st.session_state.form_saved:
        st.success("儲存成功！")
        st.session_state.form_saved = False
        time.sleep(2)
        st.session_state.page = "budget"
        st.rerun()

    data=budget_load_data()
    for i, item in enumerate(data):
        col1, col2 = st.columns([6, 1])
        
        with col1: 
            # if item["type"] == "收入":
            #     st.markdown(f"<span style='color: green;'>[{item['date']}] {item['type']} | {item['category']} | {item['amount']} 元 > {item['note']}</span>", unsafe_allow_html=True)
            # else:
            #     st.markdown(f"<span style='color: red;'>[{item['date']}] {item['type']} | {item['category']} | {item['amount']} 元 > {item['note']}</span>", unsafe_allow_html=True)
            st.write(f" {item['budget_month']}月 | 增加{item['budget_amount']} 元 ")
        with col2:
            if st.button("🗑️ 刪除", key=f"del_{i}"):
                budget_delete_record(i)
                st.rerun()
    
elif st.session_state.page == "balance":   
    st.title("本月結算")
    balance=balance()
    st.metric("本月結算", f"${balance}")
    

    # balance_data = [item for item in data if item["category"] == selected_category]
    #     else:
    #         filtered_data = data
    








    # categories = {}
    # # for item in data:
    # #     key = f"{item['type']} - {item['category']}"
    # #     categories[key] = categories.get(key, 0) + item["amount"]
    # # for key, val in categories.items():
    # #     st.write(f"{key}：${val}")
    # total = 0
    # total01= 0
    # total02 = 0
    # total03 = 0
    # total04 = 0
    # total05 = 0
    # total06 = 0
    # total07 = 0
    # total08 = 0
    # total09 = 0
    # for item in data:
    #     if item["category"] == "早餐":
    #             total01 += item["amount"]
    #     elif item["category"] == "午餐":
    #             total02 += item["amount"]
    #     elif item["category"] == "晚餐":
    #             total03 += item["amount"]
    #     elif item["category"] == "宵夜":
    #             total04 += item["amount"]
    #     elif item["category"] == "飲料":
    #             total05 += item["amount"]
    #     elif item["category"] == "文具":
    #             total06 += item["amount"]
    #     elif item["category"] == "課本":
    #             total07 += item["amount"]
    #     elif item["category"] == "遊戲":
    #             total08 += item["amount"]
    #     elif item["category"] == "其他":
    #             total09 += item["amount"]
        
        
        
    #     elif item["category"] == "午餐":
    #         if item["type"] == "支出":
    #             total02 += item["amount"]
    #         else:
    #             total02 -= item["amount"]
    #     elif item["category"] == "晚餐":
    #         if item["type"] == "收入":
    #             total03 += item["amount"]
    #         else:
    #             total03 -= item["amount"]
    #     elif item["category"] == "宵夜":
    #         if item["type"] == "收入":
    #             total04 += item["amount"]
    #         else:
    #             total04 -= item["amount"]
    #     elif item["category"] == "飲料":
    #         if item["type"] == "收入":
    #             total05 += item["amount"]
    #         else:
    #             total05 -= item["amount"]
    #     elif item["category"] == "文具":
    #         if item["type"] == "收入":
    #             total06 += item["amount"]
    #         else:
    #             total06 -= item["amount"]
    #     elif item["category"] == "課本":
    #         if item["type"] == "收入":
    #             total07 += item["amount"]
    #         else:
    #             total07 -= item["amount"]
    #     elif item["category"] == "遊戲":
    #         if item["type"] == "收入":
    #             total08 += item["amount"]
    #         else:
    #             total08 -= item["amount"]
    #     elif item["category"] == "其他":
    #         if item["type"] == "收入":
    #             total09 += item["amount"]
    #         else:
    #             total09 -= item["amount"]
            

    # st.write(f"早餐：${total01}")
    # st.write(f"午餐：${total02}")
    # st.write(f"晚餐：${total03}")
    # st.write(f"宵夜：${total04}")
    # st.write(f"飲料：${total05}")
    # st.write(f"文具：${total06}")
    # st.write(f"課本：${total07}")
    # st.write(f"遊戲：${total08}")
    # st.write(f"其他：${total09}")



# elif st.session_state.page == "achieve":
#     st.title("__查看紀錄__")
#     st.header("所有記帳紀錄")
#     data = load_data()
#     st.dataframe(data)
    





# elif st.session_state.page == "achieve":
#     st.title("__成就系統__")





# if menu1=="新增紀錄" :
#     st.title("記帳工具")

# if menu2=="成就" :
#     st.title("__成就系統__")

# if menu=="查看紀錄" :
#     st.title("查看紀錄")
# if menu=="收支統計" :
#     st.title("收支統計")



# name = st.text_input("請輸入你的名字：")
# if name:
#     st.write(f"你好阿，{name}！")












