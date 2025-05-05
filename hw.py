


import streamlit as st
import time
from utils import load_data, save_data, add_record, calculate_total

def delete_record(index):
    data = load_data()
    
    removed = data.pop(index)
    save_data(data)
    st.success(f"已刪除：{removed['date']} {removed['category']} {removed['amount']} 元")
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

# 顯示頁面內容

if st.session_state.page == "home":
    st.title("歡迎使用記帳小工具")


if st.session_state.page == "add":
    st.title("新增收支紀錄")

    with st.form("entry_form"):
        amount = st.number_input("金額", min_value=1, step=1)
        category = st.selectbox("分類", ["早餐", "午餐", "晚餐", "宵夜", "飲料", "文具", "課本", "遊戲", "其他"])
        note = st.text_input("備註")
        is_income = st.radio("收入 / 支出", ["支出", "收入"]) == "收入"
        submitted = st.form_submit_button("儲存紀錄")
        if submitted:
            st.session_state.form_saved = True
            add_record(amount, category, note, is_income)
            

    if st.session_state.form_saved:
            st.success("儲存成功！")
            st.session_state.form_saved = False
            time.sleep(2)
            st.session_state.page = "add"
            st.rerun()

elif st.session_state.page == "achieve":
    st.title("__查看紀錄__")
    st.header("所有記帳紀錄")
    data = load_data()
    if not data:
        st.info("目前沒有任何記錄。")
    else:
        for i, item in enumerate(data):
            col1, col2 = st.columns([5, 1])
            with col1:
                st.write(f" [{item['date']}] {item['type']} | {item['category']} | {item['amount']} 元 - {item['note']}")
            with col2:
                if st.button("🗑️ 刪除", key=f"del_{i}"):
                    delete_record(i)
                    st.rerun()
                  
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












