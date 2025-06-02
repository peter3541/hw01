


import streamlit as st
import time
from back import load_data, save_data, add_record, calculate_total,calculate_category_totals,add_budget,balance,budget_load_data,budget_save_data,honor,honor02,honor03
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
if st.sidebar.button("成就系統"):
    st.session_state.page = "honor"

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

    



elif st.session_state.page == "count":
    
    st.title("各類別統計")
    data = load_data()
    totals = calculate_category_totals(data)

    # 顯示結果



    for category, total in totals.items():
        st.write(f"{category}：${total}")



    
elif st.session_state.page == "budget":
    st.title("新增預算")
    
    with st.form("entry_form"):
        budget_month = st.selectbox("月份", ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"],index=datetime.now().month - 1)
        budget_amount = st.number_input("金額", min_value=1, step=1)

        
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
            st.write(f" {item['budget_month']}月 | 增加{item['budget_amount']} 元 ")
        with col2:
            if st.button("🗑️ 刪除", key=f"del_{i}"):
                budget_delete_record(i)
                st.rerun()
    
elif st.session_state.page == "balance":   
    st.title("本月結算")
    balance=balance()
    st.metric("本月結算", f"${balance}")
    
    

elif st.session_state.page == "honor":   
    st.markdown("<h1 class='honor'>>>>成就紀錄<<<</h1>", unsafe_allow_html=True)
    qwe,total=honor()  
    st.markdown("<h1 class='honor01'>成就➊</h1>", unsafe_allow_html=True)

    col5, col6 = st.columns([6, 2])
    with col5: 
            st.markdown("<h1 class='honor02'>花費低於1萬元</h1>", unsafe_allow_html=True)
    with col6:
        if qwe=="01ok":
            st.markdown("<h1 class='honor03'>達成</h1>", unsafe_allow_html=True)
            st.write(f"~本月總花費為{total}元") 
        else:
            st.markdown("<h1 class='honor04'>未達成</h1>", unsafe_allow_html=True)
            st.write(f"~本月總花費為{total}元") 
    qwe=honor02() 
    st.markdown("<h1 class='honor01'>成就➋</h1>", unsafe_allow_html=True)
    col7, col8 = st.columns([6, 2])
    with col7:
        st.markdown("<h1 class='honor02'>花費低於預算</h1>", unsafe_allow_html=True)
    with col8:
        balance=balance()
        if qwe=="02ok":
            st.markdown("<h1 class='honor03'>達成</h1>", unsafe_allow_html=True)
            st.write(f"~餘額為{balance}元") 
        else:
            st.markdown("<h1 class='honor04'>未達成</h1>", unsafe_allow_html=True)
            st.write(f"~餘額為{balance}元")
            
    qwe,total=honor03() 
    st.markdown("<h1 class='honor01'>成就➌</h1>", unsafe_allow_html=True)
    col7, col8 = st.columns([6, 2])
    with col7:
        st.markdown("<h1  class='honor02'>本月花費低於上月</h1>", unsafe_allow_html=True)
    with col8:
        if qwe=="03ok":
            st.markdown("<h1 class='honor03'>達成</h1>", unsafe_allow_html=True)
            st.write(f"~較上月少了{total}元") 
        else:
            st.markdown("<h1 class='honor04'>未達成</h1>", unsafe_allow_html=True)
            st.write(f"~比上月多花了{total}元")
