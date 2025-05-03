import streamlit as st
# from menu import menu



st.sidebar.page_link("app.py", label="Switch accounts")
st.sidebar.page_link("pages/product.py", label="제품 정보")
st.sidebar.page_link("pages/component.py", label="자재 정보")
st.sidebar.page_link("pages/user.py", label="자재 소요량")
st.sidebar.page_link("pages/user.py", label="자재 명세서")
st.sidebar.page_link("pages/user.py", label="코스맥스 재고")