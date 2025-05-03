import streamlit as st
import pandas as pd
from menu import menu_with_redirect
# import airtable
from pyairtable import Api
# Redirect to app.py if not logged in, otherwise show the navigation menu
st.set_page_config(layout="wide")
menu_with_redirect()



api_key = 'patqEfN06y9QLUoS0.0ff77915af3ff09a6aea08f2b64da60016c567129cea7448c8d903265d5cda71'


api_key = 'patqEfN06y9QLUoS0.0ff77915af3ff09a6aea08f2b64da60016c567129cea7448c8d903265d5cda71'
base_id= 'appESzks3l70ngxgd'
cosmax_table = 'tbloZpZ5QZY6nZPD0'
component_table = 'tbl8uwQUhuWQMlJtf'
product_table ='tblreG6m3bTRYMeLy'


def get_product_list():
    api = Api(api_key)
    table = api.table(base_id ,product_table)
    result = table.all()
    return [r['fields'] for r in result]

product_list = get_product_list()

# left, right = st.columns((10, 20))
st.title("자재소요량(MR)")

# 세션 상태 초기화
if 'df_left' not in st.session_state:
    st.session_state.df_left = pd.DataFrame(product_list).assign(선택=False)
if 'df_right' not in st.session_state:
    st.session_state.df_right = pd.DataFrame({
        '제품코드': [],
        '제품명': [],
        '단위': [],
        '수량': [],
    }).assign(선택=False)

# Streamlit 앱 레이아웃
st.title("DataFrame 간 데이터 이동")

# 3개의 컬럼 생성: 왼쪽 DataFrame, 버튼, 오른쪽 DataFrame
col1,_, col2,_, col3 = st.columns([10,0.5, 1,0.5, 10])

# 왼쪽 DataFrame
with col1:
    st.subheader("왼쪽 DataFrame")
    edited_left = st.data_editor(
        st.session_state.df_left,
        key="left_df",
        num_rows="fixed",
        # use_container_width=True,
        column_order=['선택', '제품코드', '제품명', '단위'],
        hide_index=True,
        column_config={
        "선택": st.column_config.Column(
            width=1
        )
        }
    )

    # 편집된 데이터로 세션 상태 업데이트
    if not edited_left.equals(st.session_state.df_left):
        st.session_state.df_left = edited_left.copy()

# 가운데 버튼
with col2:
    st.write("")  # 여백
    st.write("")  # 여백
    st.write("")  # 여백
    # 오른쪽으로 이동 버튼
    if st.button("→",use_container_width=True):
        selected_rows = st.session_state.df_left[st.session_state.df_left['선택'] == True]
        if not selected_rows.empty:
            # 선택된 행을 오른쪽으로 이동
            rows_to_move = selected_rows.drop(columns=['선택']).copy()
            st.session_state.df_right = pd.concat([
                st.session_state.df_right.drop(columns=['선택']),
                rows_to_move
            ], ignore_index=True).assign(선택=False)
            # 왼쪽에서 선택된 행 삭제
            st.session_state.df_left = st.session_state.df_left[
                st.session_state.df_left['선택'] == False
            ].drop(columns=['선택']).reset_index(drop=True).assign(선택=False)
            st.rerun()

    # 왼쪽으로 이동 버튼
    if st.button("←",use_container_width=True):
        selected_rows = st.session_state.df_right[st.session_state.df_right['선택'] == True]
        if not selected_rows.empty:
            # 선택된 행을 왼쪽으로 이동
            rows_to_move = selected_rows.drop(columns=['선택']).copy()
            st.session_state.df_left = pd.concat([
                st.session_state.df_left.drop(columns=['선택']),
                rows_to_move
            ], ignore_index=True).assign(선택=False)
            # 오른쪽에서 선택된 행 삭제
            st.session_state.df_right = st.session_state.df_right[
                st.session_state.df_right['선택'] == False
            ].drop(columns=['선택']).reset_index(drop=True).assign(선택=False)
            st.rerun()

# 오른쪽 DataFrame
with col3:
    st.subheader("오른쪽 DataFrame")
    edited_right = st.data_editor(
        st.session_state.df_right,
        key="right_df",
        num_rows="fixed",
        # use_container_width=True,
        column_order=['선택', '제품코드', '제품명', '단위', '수량'],
        hide_index=True
    )
    # 편집된 데이터로 세션 상태 업데이트
    if not edited_right.equals(st.session_state.df_right):
        st.session_state.df_right = edited_right.copy()

# 병합 버튼
if st.button("자재코드로 병합"):
    merged_df = pd.merge(
        st.session_state.df_left.drop(columns=['선택']),
        st.session_state.df_right.drop(columns=['선택']),
        on='자재코드',
        how='inner',
        suffixes=('_left', '_right')
    )
    desired_columns = ['자재코드', '가격_left', '수량_left', '가격_right', '수량_right']
    merged_df = merged_df[desired_columns]
    st.subheader("병합된 DataFrame")
    st.dataframe(merged_df, use_container_width=True)