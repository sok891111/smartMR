import streamlit as st
import pandas as pd
from menu import menu_with_redirect
# import airtable
from pyairtable import Api
from datetime import datetime
# Redirect to app.py if not logged in, otherwise show the navigation menu
st.set_page_config(layout="wide", page_title='자재 발주 시스템(smartMR)')
menu_with_redirect()



api_key = 'patqEfN06y9QLUoS0.0ff77915af3ff09a6aea08f2b64da60016c567129cea7448c8d903265d5cda71'


api_key = 'patqEfN06y9QLUoS0.0ff77915af3ff09a6aea08f2b64da60016c567129cea7448c8d903265d5cda71'
base_id= 'appESzks3l70ngxgd'
cosmax_table = 'tbloZpZ5QZY6nZPD0'
component_table = 'tbl8uwQUhuWQMlJtf'
product_table ='tblreG6m3bTRYMeLy'
component_table = 'tbl8uwQUhuWQMlJtf'
usage_table_id = 'tbltPILlWV5S9Bshj'

fixed_date = datetime(2025, 5, 3)

# "YYYY년 MM월 DD일" 형식으로 포맷팅
today = fixed_date.strftime("%Y년 %m월 %d일")

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

@st.cache_data(ttl=600)  
def get_product_list():
    api = Api(api_key)
    table = api.table(base_id ,product_table)
    result = table.all()
    return [r['fields'] for r in result]

@st.cache_data(ttl=600)  
def get_component_list():
    api = Api(api_key)
    table = api.table(base_id ,component_table)
    result = table.all()
    return [r['fields'] for r in result]    

@st.cache_data(ttl=600)  
def get_usage_list():
    api = Api(api_key)
    table = api.table(base_id ,usage_table_id)
    result = table.all()
    return [r['fields'] for r in result]

def update_warning(show):
    st.session_state.show_warning = show

if 'show_warning' not in st.session_state:
    st.session_state.show_warning = True

spinner_placeholder = st.empty()
with spinner_placeholder.container():
    st.markdown('<div class="spinner-overlay"><div class="spinner"></div></div>', unsafe_allow_html=True)
    product_list = get_product_list()
    component_list = get_component_list()
    component_usage_list = get_usage_list()

    # left, right = st.columns((10, 20))
    

    product_df = pd.DataFrame(product_list)
    usage_df = pd.DataFrame(component_usage_list)
    component_df = pd.DataFrame(component_list)
spinner_placeholder.empty()

st.title("자재소요량(MR)")

# 행 선택을 위한 multiselect
options = [f"[{row['제품코드']}] {row['제품명']}" for _, row in product_df.iterrows()]
selected_product = st.multiselect("제품 선택" ,options, key="product_select")


selected_codes = [opt.split(' ')[0].replace('[','').replace(']','').strip() for opt in selected_product]


st.info("셀 편집 후 Enter 키를 누르거나 빈칸을 후 저장 버튼을 클릭하여 데이터를 반영합니다.")
st.subheader("주문 수량 입력" ,divider='grey')

rows_to_move = product_df[product_df['제품코드'].isin(selected_codes)].copy()

input_df = st.data_editor(
    rows_to_move.assign(수량=1),
    num_rows="fixed",
    # use_container_width=True,
    column_order=[ '제품코드', '제품명', '단위' , '수량'],
    hide_index=True,
    disabled=["제품코드" , '제품명' ,'단위'],
    column_config={
        "수량": st.column_config.NumberColumn(
            "주문 수량",
            help="주문 수량을 입력하세요",
            min_value=0,
            max_value=5000,
            step=1
        )
    },
    )

if sum(input_df['수량']) == 0 :
    
    st.warning("제품 수량을 입력하지 않았습니다. 수량을 입력하시면 다음 단계 작업이 진행됩니다.", icon="⚠️")
else:
    update_warning(False)
    filtered_df = usage_df[usage_df['제품번호'].isin(selected_codes)]

    merged_df = pd.merge(filtered_df, component_df, on='자재코드', how='inner')
    cal_df = merged_df[[ '제품번호' , '자재코드' , '자재명' , '소요량' , '단위','단가' , '재고량' ,'업체코드' ]].copy()
    cal_df = cal_df.astype({'소요량': 'int', '단가': 'int', '재고량': 'int'})

    for _, row in input_df.iterrows():
        
        cal_df.loc[cal_df['제품번호'] == row['제품코드'] , '소요량'] = cal_df.loc[cal_df['제품번호'] == row['제품코드'] , '소요량'] * row['수량']
        

    num_df = cal_df.groupby('자재코드')[['소요량', '재고량']].sum().reset_index()

    final_df = pd.merge(num_df, component_df[['자재코드', '자재명', '단위' , '단가' , '업체코드']], on='자재코드', how='inner')
    final_df['필요량'] = final_df['소요량'] - final_df['재고량']
    final_df['발주량'] = 0

    st.subheader("자제 소요량 계산" ,divider='grey')
    order_df = st.data_editor(
        final_df,
        num_rows="fixed",
        # use_container_width=True,
        column_order=[ '자재코드', '자재명', '소요량' , '단위' , '단가' , '재고량' , '필요량' , '발주량' , '금액' , '업체코드'],
        hide_index=True,
        disabled=["자재코드" , '자재명' ,'소요량' , '단위' , '단가' , '재고량' , '필요량' , '금액' , '업체코드'],
        column_config={
            "발주량": st.column_config.NumberColumn(
                "발주량",
                help="주문 수량을 입력하세요",
                min_value=0,
                max_value=10000,
                step=1
            )
        },
        )

    if sum(order_df['발주량']) == 0 :
    
        st.warning("발주량을 입력하지 않았습니다. 수량을 입력하시면 다음 단계 작업이 진행됩니다.", icon="⚠️")
    # st.dataframe(fina_df)
    else:
        company_list = order_df['업체코드'].drop_duplicates().to_list()
        st.subheader("업체별 발주서" ,divider='grey')
        tabs = st.tabs(company_list)
        for index, comp in enumerate(company_list):
            with tabs[index]:
                
                # HTML 코드를 Streamlit에 표시
                html_code = f"""
                <!DOCTYPE html>
                <html lang="ko">
                <style>
                html{{
                    background: white;
                  
                }}
                </style>
                <head>
                    <meta charset="UTF-8">
                    <style>
                        body {{ font-family: Arial, sans-serif; margin: 20px; line-height: 1.6; }}
                        .title {{ text-align: center; font-size: 50px; font-weight: bold; margin-bottom: 20px; text-decoration: underline;}}
                        .info-container {{ display: flex; justify-content: space-between; margin-bottom: 20px; }}
                        .info-box {{ text-align: center;  }}
                        .info-box-right {{ text-align: center;  }}
                        .info-box h3 {{ margin-top: 25px; font-size: 16px; padding-bottom: 5px; }}
                        .info-box p {{ margin: 5px 0; }}
                        table {{
                            width: 100%;
                            border-collapse: collapse;
                            font-family: Arial, sans-serif;
                        }}
                        td {{
                            border: 2px solid black;
                            padding: 10px;
                            text-align: center;
                            
                            font-size: 14px;
                        }}
                        .label {{
                          
                            font-weight: bold;
                            background-color: #f4a460; 
                        }}
                        .value {{
                            
                        }}
                        
                        .footer {{ display: flex; justify-content: space-between; border-top: 1px solid #000; padding-top: 10px; }}
                        .footer div {{ width: 100%; text-align: center; }}
                        .vertical-text {{
                      text-align: center; /* 가운데 정렬 */
                         font-weight: bold;
                            background-color: #f4a460; 
                    }}
                table {{
                      border-collapse: collapse;
                      border: 2px solid black; /* 외곽 테두리: 진하게 */
                    }}
                /* .bom_body 아래 테이블에만 적용 */
                    .bom_body table {{
                      border-collapse: collapse; /* 테두리 겹치기 */
                    }}
                    .bom_body table th,
                    .bom_body table td {{
                    height: 30px;
                      border: 1px solid #ccc; /* 내부 테두리: 연하게 (#ccc는 연한 회색) */
                      padding: 10px; /* 셀 내부 여백 */
                    }}
                    /* 외곽 테두리와 내부 테두리 겹침 조정 */
                    .bom_body table th:first-child,
                    .bom_body table td:first-child {{
                      border-left: 1px solid #ccc;
                    }}
                    .bom_body table th:last-child,
                    .bom_body table td:last-child {{
                      border-right: 1px solid #ccc;
                    }}
                    .bom_body table tr:first-child th,
                    .bom_body table tr:first-child td {{
                      border-top: 1px solid #ccc;
                    }}
                    .bom_body table tr:last-child th,
                    .bom_body table tr:last-child td {{
                      border-bottom: 1px solid #ccc;
                    }}

                    </style>
                </head>
                <body>
                    <div class="title">&nbsp;&nbsp;발&nbsp;&nbsp;&nbsp;주&nbsp;&nbsp;&nbsp;서&nbsp;&nbsp;</div>
                    <div class="info-container">
                        
                        <div class="info-box" style="max-width:35%">
                            <table>
                                <tr>
                                    <td class="label">견적서</td>
                                    <td class="value" >{comp}</td>
                                </tr>
                                <tr>
                                    <td class="label">발주일자</td>
                                    <td class="value" >{today}</td>
                                </tr>
                                <tr>
                                    <td colspan=2></td>
                                </tr>
                            </table>
                            <div class="info-box" style="width: 100%; text-align: left;">
                                <h3>아래와 같이 발주합니다</h3>
                            </div>
                        </div>
                        <div class="info-box-right">
                            <table>
                                <tr>
                                    <td class="vertical-text" colspan=4 rowspan=5>공<br/><br/>급<br/><br/>자<br/></td>
                                    
                                </tr>
                                <tr>
                                    <td class="label">등록번호</td>
                                    <td class="value" colspan=3 style="font-weight: bold;font-size:18px">159-86-02338</td>
                                </tr>
                                <tr>
                                    <td class="label">상 호</td>
                                    <td class="value" >주식회사 쿠퍼스테이션</td>
                                    <td class="label">대표자</td>
                                    <td class="value">천은경</td>
                                </tr>
                                <tr>
                                    <td class="label">주 소</td>
                                    <td class="value" colspan=3>서울시 강남구 강남대로152길 14 5층 506호</td>
                                </tr>
                                <tr>
                                    <td class="label">업 태</td>
                                    <td class="value" >도매 및 소매업</td>
                                    <td class="label">업 종</td>
                                    <td class="value">화장품</td>
                                </tr>
                            </table>
                        </div>
                    </div>
                    <div class="bom_body">
                    <table>
                    <colgroup>
                                <col style="width: 40%;"> <!-- 품 명 열 -->
                                <col style="width: 12%">  <!-- 수량 열 -->
                                <col style="width: 12%;"> <!-- 공급단가 열 -->
                                <col style="width: 12%;"> <!-- 공급가액 열 -->
                                <col style="width: 12%;">  <!-- 부가세 열 -->
                                <col style="width: 12%;"> <!-- 합계 열 -->
                              </colgroup>
                        <thead>
                            <tr>
                                <th>품&nbsp;&nbsp;명</th>
                                <th>수량</th>
                                <th>공급단가</th>
                                <th>공급가액</th>
                                <th>부가세</th>
                                <th>합계</th>
                            </tr>
                        </thead>
                        <tbody>"""
                # st.write(order_df)
                comp_df = order_df[order_df['업체코드'] == comp]
                for _, row in comp_df.iterrows():
                    html_code += f"""
                            <tr>
                                <td>{row['자재명']}</td>
                                <td>{row['발주량']}</td>
                                <td>{row['단가']}</td>
                                <td>{row['단가']}</td>
                                <td>0</td>
                                <td>{row['단가']}</td>
                            </tr>
                            """
                total_cost = comp_df['단가'].sum()
                html_code += f"""
                            <tr>
                                <td></td>
                                <td></td>
                                <td></td>
                                <td></td>
                                <td></td>
                                <td></td>
                            </tr>
                            <tr>
                                <td></td>
                                <td></td>
                                <td></td>
                                <td></td>
                                <td></td>
                                <td></td>
                            </tr>
                            <tr style="border-top: 3px double black;">
                                <td>합 계</td>
                                <td>{total_cost}</td>
                                <td></td>
                                <td></td>
                                <td></td>
                                <td></td>
                            </tr>
                            <tr style="border-top: 2px solid black;">
                                <td colspan=6>특 기 사 항</td>
                            </tr>
                            <tr style="height: 100px;">
                                <td colspan=6></td>
                            </tr>
                        </tbody>
                    </table>
                    </div>
                    
                    <div class="footer">
                        <div class="bom_body">
                        <table>
                                <tr>
                                <th>전화번호</th>
                                <td>010-9213-2746</td>
                                <th>FAX</th>
                                <td></td>
                                <th>담당자</th>
                                <td>김수진</td>
                                <tr>
                            </table>
                        </div>
                    </div>
                </body>
                </html>
                """

                # Streamlit에서 HTML 표시
                st.components.v1.html(html_code, height=1200, scrolling=True)    

                                # Streamlit에서 HTML 표시
                js_code = f"""
                <script>
                function openPopup() {{
                    var win = window.open('', 'Popup', 'width=800,height=600');
                    win.document.write(`
                        {html_code.replace('<body>','<body onload="window.print();"/>')}
                    `);

                    win.document.close();
                }}
                </script>
                <button onclick="openPopup()" style="padding: 10px 20px; background-color: #4CAF50; color: white; border: none; cursor: pointer; border-radius: 4px;">
                    PDF 인쇄
                </button>
                """

                # HTML 렌더링
                st.components.v1.html(js_code, height=50)




