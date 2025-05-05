import streamlit as st
import pandas as pd
from menu import menu_with_redirect
from pyairtable import Api
# Redirect to app.py if not logged in, otherwise show the navigation menu
st.set_page_config(layout="wide", page_title='자재 발주 시스템(smartMR)')
menu_with_redirect()



api_key = 'patqEfN06y9QLUoS0.0ff77915af3ff09a6aea08f2b64da60016c567129cea7448c8d903265d5cda71'
base_id= 'appESzks3l70ngxgd'
cosmax_table = 'tbloZpZ5QZY6nZPD0'
component_table = 'tbl8uwQUhuWQMlJtf'




# 커스텀 CSS로 중앙 스피닝 스타일 정의
st.markdown(
    """
    <style>
    .spinner-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.3); /* 반투명 배경 */
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 9999;
    }
    .spinner {
        border: 8px solid #f3f3f3;
        border-top: 8px solid #3498db;
        border-radius: 50%;
        width: 60px;
        height: 60px;
        animation: spin 1s linear infinite;
    }
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    </style>
    """,
    unsafe_allow_html=True
)



def get_stock_list():
    api = Api(api_key)
    table = api.table(base_id , cosmax_table)
    return table.all()

# at = airtable.Airtable('appESzks3l70ngxgd', api_key)
stock_list = get_stock_list()


# left, right = st.columns((10, 20))
st.title("코스맥스 재고")

uploaded_file = st.file_uploader("코스맥스 재고 CSV 파일을 선택하세요", type=["csv"])
if uploaded_file is not None:
    # CSV 파일을 DataFrame으로 읽기
    try:
        spinner_placeholder = st.empty()
        with spinner_placeholder.container():
            st.markdown('<div class="spinner-overlay"><div class="spinner"></div></div>', unsafe_allow_html=True)        
            upload_df = pd.read_csv(uploaded_file)
            
            upload_df = upload_df.fillna('0').astype(str)
            #1. 먼저 삭제
            api = Api(api_key)
            table = api.table(base_id , cosmax_table)
            table.batch_delete([r['id'] for r in stock_list])


            #2. csv 파일 upload
            new_data = []
            component_data = []
            for index, row in upload_df.iterrows():
                new_data.append({col: row[col] for col in row.index})
                if row['품목명'] != '(삭제)':
                    component_data.append({
                        '자재코드' : row['품목코드'],
                        '자재명' : row['품목명'],
                        '단위' : 'EA',
                        '재고량' : row['가용재고'],
                        '업체코드' : row['협력업체명']
                        })
            # st.write(new_data)
            table.batch_create(new_data)
            st.success("CSV 파일이 성공적으로 업로드되었습니다!")
            
            #3.재고 정보 삭제
            c_table = api.table(base_id , component_table)
            component_list = c_table.all()
            c_table.batch_delete([r['id'] for r in component_list])

            #4.재고 정보 입력
            c_table.batch_create(component_data)
            st.success("재고 정보가 정상 반영되었습니다.")

            stock_list = get_stock_list()
        spinner_placeholder.empty()


    except Exception as e:
        st.error(f"CSV 파일을 읽는 중 오류 발생: {e}")



st.info("upload 된 CSV 파일의 재고 정보는 자재정보에 자동 반영 됩니다.")
st.subheader('현재 코스맥스 재고 정보', divider='grey')
data = pd.DataFrame(r['fields'] for r in stock_list)
st.dataframe(data , height=1000)



