import streamlit as st


def authenticated_menu():
    # Show a navigation menu for authenticated users
    st.sidebar.page_link("app.py", label="HOME")
    st.sidebar.page_link("pages/product.py", label="제품 정보")
    st.sidebar.page_link("pages/component.py", label="자재 정보")
    st.sidebar.page_link("pages/component_usage.py", label="자재 명세서")
    st.sidebar.page_link("pages/bom.py", label="자재 소요량")
    st.sidebar.page_link("pages/cosmax.py", label="코스맥스 재고")
    st.sidebar.page_link("pages/chat.py", label="Chat with AI")
    # st.sidebar.page_link("pages/test.py", label="test")


def unauthenticated_menu():
    # Show a navigation menu for unauthenticated users
    st.sidebar.page_link("app.py", label="Log in")


def menu():
    # Determine if a user is logged in or not, then show the correct
    # navigation menu
    # if "role" not in st.session_state or st.session_state.role is None:
        # unauthenticated_menu()
        # return
    st.markdown(
        """
        <style>
    [class^="_profileImage"] {
        display: none !important;
    }
    .stAppToolbar {
    display: none !important;
    }
     /* 상단 로딩 줄 숨기기 */
    div[data-testid="stStatusWidget"] {
        visibility: hidden !important;
    }
    /* 추가적인 Streamlit 브랜딩 요소 숨기기 (선택사항) */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    .stDecoration{
        display:none !important;
    }
      [class^="_profileContainer"] {
        display: none !important;
    }

    
    
        </style>
        """,
        unsafe_allow_html=True
    )
    authenticated_menu()


def menu_with_redirect():
    # Redirect users to the main page if not logged in, otherwise continue to
    # render the navigation menu
    # if "role" not in st.session_state or st.session_state.role is None:
        # st.switch_page("app.py")
    menu()
