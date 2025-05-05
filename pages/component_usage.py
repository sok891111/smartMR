import streamlit as st
import pandas as pd
from menu import menu_with_redirect
# import airtable
from pyairtable import Api
st.set_page_config(layout="wide", page_title='자재 발주 시스템(smartMR)')
# Redirect to app.py if not logged in, otherwise show the navigation menu
menu_with_redirect()

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


api_key = 'patqEfN06y9QLUoS0.0ff77915af3ff09a6aea08f2b64da60016c567129cea7448c8d903265d5cda71'
base_id= 'appESzks3l70ngxgd'
usage_table_id = 'tbltPILlWV5S9Bshj'

api = Api(api_key)

@st.cache_data(ttl=1200)  
def get_component_list():
    api = Api(api_key)
    table = api.table(base_id, 'tbl8uwQUhuWQMlJtf')
    return table.all()


@st.cache_data(ttl=1200)
def get_product_list():
    api = Api(api_key)
    table = api.table(base_id, 'tblreG6m3bTRYMeLy')
    return table.all()

@st.cache_data(ttl=1200)
def get_usage_list():
	api = Api(api_key)
	table = api.table(base_id ,usage_table_id)
	result = table.all()
	df = pd.DataFrame(r['fields'] for r in result)
	df['id'] = [r['id'] for r in result]

	return df

component_list = get_component_list()
product_list = get_product_list()
# component_usage_list = get_usage_list()


st.title("자재명세서")


product = pd.DataFrame(r['fields'] for r in product_list)
component = pd.DataFrame(r['fields'] for r in component_list)
component_usage = get_usage_list()


# st.divider()  
st.subheader("제품을 선택하세요." ,divider='grey')
st.info("아래 상품 표에서 첫번째 컬럼을 클릭하여 상품을 선택해주세요.")
event = st.dataframe(product , selection_mode='single-row',on_select="rerun" , hide_index=True,)

select_product = event.selection.rows

if len(select_product)> 0:
	st.info("셀 편집 후 Enter 키를 누르거나 빈칸을 추가한 후 저장 버튼을 클릭하여 데이터를 반영합니다. ( table over 시 우측상단에 표시되는 toolbar 를 통해 데이터 조작 가능 )")
	col1,col2 = st.columns([2, 3])  # Create two columns: one for spacing, one for buttons
	with col1:
		product_code = product.iloc[select_product , 0 ].item()
		
		filtered_df= component_usage[component_usage.제품번호 == product_code ]
		merged_df = pd.merge(filtered_df, component, on='자재코드', how='inner')
		merged_df = merged_df[[ '자재코드' , '소요량' , '자재명' ,'id'  ]]

		st.subheader("선택된 상품의 자재 소요량" )
		# st.divider()  
		edited_df = st.data_editor(
		    merged_df,
			num_rows="dynamic",
			key="data_editor",
			column_config={"id": None}
		    
		)
		
		_,button_left = st.columns([5, 1]) 
		with button_left:

			if st.button('저장' , use_container_width=True) :

				spinner_placeholder = st.empty()
				with spinner_placeholder.container():
					st.markdown('<div class="spinner-overlay"><div class="spinner"></div></div>', unsafe_allow_html=True)
					
					
					table = api.table(base_id, usage_table_id)
					#1.모두 삭제 
					if len(merged_df.id.to_list()) > 0:
						table.batch_delete(merged_df.id.to_list())
					#2. 모두 추가
					new_data = []
					for index, row in edited_df.iterrows():
						new_data.append({
						"제품번호": product_code,
						"소요량": row['소요량'],
						"자재코드": row['자재코드'],
						}
						)
					table.batch_create(new_data)
					st.cache_data.clear()
					st.cache_resource.clear()
					st.rerun()    
					
				# 시간이 걸리는 작업 시뮬레이션
				# 스피닝 제거
				spinner_placeholder.empty()
				
				st.toast('저장 완료되었습니다.', icon='🎉')
	
					

				
				

				

	with col2:
		st.subheader("자재 정보" )
		st.dataframe(component)
