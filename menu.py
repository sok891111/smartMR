import streamlit as st


def authenticated_menu():
    # Show a navigation menu for authenticated users
    st.sidebar.page_link("app.py", label="Switch accounts")
    st.sidebar.page_link("pages/product.py", label="제품 정보")
    st.sidebar.page_link("pages/component.py", label="자재 정보")
    st.sidebar.page_link("pages/component_usage.py", label="자재 명세서")
    st.sidebar.page_link("pages/bom.py", label="자재 소요량")
    st.sidebar.page_link("pages/cosmax.py", label="코스맥스 재고")
    st.sidebar.page_link("pages/test.py", label="test")


def unauthenticated_menu():
    # Show a navigation menu for unauthenticated users
    st.sidebar.page_link("app.py", label="Log in")


def menu():
    # Determine if a user is logged in or not, then show the correct
    # navigation menu
    # if "role" not in st.session_state or st.session_state.role is None:
        # unauthenticated_menu()
        # return
    authenticated_menu()


def menu_with_redirect():
    # Redirect users to the main page if not logged in, otherwise continue to
    # render the navigation menu
    # if "role" not in st.session_state or st.session_state.role is None:
        # st.switch_page("app.py")
    menu()