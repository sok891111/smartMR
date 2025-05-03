import streamlit as st
from menu import menu
st.set_page_config(layout="wide")
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
    

menu() # Render the dynamic menu!