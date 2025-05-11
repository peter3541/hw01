
import streamlit as st
from back import load_data, save_data, add_record, calculate_total

st.set_page_config(page_title="簡易記帳小幫手", layout="centered")

st.title("📒 簡易記帳小幫手")

# 側邊欄選單
menu = st.sidebar.selectbox("請選擇功能", ["新增紀錄", "查看紀錄", "收支統計"])

if menu == "新增紀錄":
    st.header("📝 新增收支紀錄")
    with st.form("entry_form"):
        amount = st.number_input("金額", min_value=1, step=1)
        category = st.selectbox("分類", ["餐飲", "交通", "娛樂", "薪水", "其他"])
        note = st.text_input("備註")
        is_income = st.radio("收入 / 支出", ["支出", "收入"]) == "收入"
        submitted = st.form_submit_button("儲存紀錄")
        if submitted:
            add_record(amount, category, note, is_income)
            st.success("✅ 紀錄已儲存！")


            

elif menu == "查看紀錄":
    st.header("📊 所有記帳紀錄")
    data = load_data()
    if data:
        st.dataframe(data)
    else:
        st.info("尚無紀錄，請先新增一筆資料！")

elif menu == "收支統計":
    st.header("💰 目前帳戶總額")
    data = load_data()
    total = calculate_total(data)
    st.metric("總額", f"${total}")

    st.subheader("📂 各類別統計")
    categories = {}
    for item in data:
        key = f"{item['type']} - {item['category']}"
        categories[key] = categories.get(key, 0) + item["amount"]

    for key, val in categories.items():
        st.write(f"{key}：${val}")




