import streamlit as st
from menu import menu
st.set_page_config(layout="wide", page_title='자재 발주 시스템(smartMR)')
# Initialize st.session_state.role to None
if "role" not in st.session_state:
    st.session_state.role = 'admin'

# Retrieve the role from Session State to initialize the widget
# st.session_state._role = 'admin'

# def set_role():
#     # Callback function to save the role selection to Session State
#     st.session_state.role = st.session_state._role



# if st.session_state.role in ["admin", "super-admin"]:
#     st.sidebar.page_link("pages/admin.py", label="Manage users")
#     st.sidebar.page_link(
#         "pages/super-admin.py",
#         label="Manage admin access",
#         disabled=st.session_state.role != "super-admin",
    

st.title('자재 발주시스템(smartMR)')
st.link_button('Data 정보' , 'https://airtable.com/appESzks3l70ngxgd/shrWVfF0tqycy0VVL')
# URL로 이미지 표시
st.image("https://cherejeanne.com/web/upload/NNEditor/20241211/69011e14e7eb809ecef81a6a5bb8d2ed.jpg", caption="cherejeanne")


menu() # Render the dynamic menu!