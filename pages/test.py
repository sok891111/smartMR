import streamlit as st
import pandas as pd
from menu import menu_with_redirect
import airtable


import streamlit as st
import pandas as pd
st.set_page_config(layout="wide", page_title='자재 발주 시스템(smartMR)')
menu_with_redirect()
# 세션 상태 초기화
if 'df_left' not in st.session_state:
    st.session_state.df_left = pd.DataFrame({
        '자재코드': ['A001', 'A002', 'A003'],
        '수량': [10, 20, 30],
        '가격': [1000, 2000, 3000]
    })
if 'df_right' not in st.session_state:
    st.session_state.df_right = pd.DataFrame({
        '자재코드': ['A004'],
        '수량': [40],
        '가격': [4000]
    })

# Streamlit 앱 레이아웃
st.title("DataFrame 간 데이터 이동")

# 3개의 컬럼 생성: 왼쪽 DataFrame, 버튼, 오른쪽 DataFrame
col1, col2, col3 = st.columns([4, 1, 4])

# 왼쪽 DataFrame
with col1:
    st.subheader("왼쪽 DataFrame")
    # DataFrame 표시 (편집 불가)
    st.dataframe(
        st.session_state.df_left,
        use_container_width=True,
        column_order=['자재코드', '가격', '수량'],
        hide_index=False
    )
    # 행 선택을 위한 multiselect
    left_options = [f"{row['자재코드']} (수량: {row['수량']}, 가격: {row['가격']})"
                    for _, row in st.session_state.df_left.iterrows()]
    selected_left = st.multiselect("왼쪽에서 이동할 행 선택", left_options, key="left_select")

# 가운데 버튼
with col2:
    st.write("")  # 여백
    st.write("")  # 여백
    # 오른쪽으로 이동 버튼
    if selected_left:
        # 선택된 자재코드 추출
        selected_codes = [opt.split(' ')[0] for opt in selected_left]
        # 선택된 행을 오른쪽으로 이동
        rows_to_move = st.session_state.df_left[
            st.session_state.df_left['자재코드'].isin(selected_codes)
        ].copy()
        st.session_state.df_right = pd.concat([
            st.session_state.df_right,
            rows_to_move
        ], ignore_index=True)
        # 왼쪽에서 선택된 행 삭제
        st.session_state.df_left = st.session_state.df_left[
            ~st.session_state.df_left['자재코드'].isin(selected_codes)
        ].reset_index(drop=True)
        st.rerun()

    # 왼쪽으로 이동 버튼
    if st.button("←", use_container_width=True):
        if selected_right:
            # 선택된 자재코드 추출
            selected_codes = [opt.split(' ')[0] for opt in selected_right]
            # 선택된 행을 왼쪽으로 이동
            rows_to_move = st.session_state.df_right[
                st.session_state.df_right['자재코드'].isin(selected_codes)
            ].copy()
            st.session_state.df_left = pd.concat([
                st.session_state.df_left,
                rows_to_move
            ], ignore_index=True)
            # 오른쪽에서 선택된 행 삭제
            st.session_state.df_right = st.session_state.df_right[
                ~st.session_state.df_right['자재코드'].isin(selected_codes)
            ].reset_index(drop=True)
            st.rerun()

# 오른쪽 DataFrame
with col3:
    st.subheader("오른쪽 DataFrame")
    # DataFrame 표시 (편집 불가)
    st.dataframe(
        st.session_state.df_right,
        use_container_width=True,
        column_order=['자재코드', '가격', '수량'],
        hide_index=False
    )
    # 행 선택을 위한 multiselect
    right_options = [f"{row['자재코드']} (수량: {row['수량']}, 가격: {row['가격']})"
                     for _, row in st.session_state.df_right.iterrows()]
    selected_right = st.multiselect("오른쪽에서 이동할 행 선택", right_options, key="right_select")

# 병합 버튼
if st.button("자재코드로 병합"):
    merged_df = pd.merge(
        st.session_state.df_left,
        st.session_state.df_right,
        on='자재코드',
        how='inner',
        suffixes=('_left', '_right')
    )
    desired_columns = ['자재코드', '가격_left', '수량_left', '가격_right', '수량_right']
    merged_df = merged_df[desired_columns]
    st.subheader("병합된 DataFrame")
    st.dataframe(merged_df, use_container_width=True)



import streamlit as st

# HTML 코드를 Streamlit에 표시
html_code = """
<!DOCTYPE html>
<html lang="ko">
<style>
html{
    background: white;
}
</style>
<head>
    <meta charset="UTF-8">
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; line-height: 1.6; }
        .title { text-align: center; font-size: 50px; font-weight: bold; margin-bottom: 20px; text-decoration: underline;}
        .info-container { display: flex; justify-content: space-between; margin-bottom: 20px; }
        .info-box {  text-align: center;  }
        .info-box-right { text-align: center;  }
        .info-box h3 { margin-top: 25px; font-size: 16px; padding-bottom: 5px; }
        .info-box p { margin: 5px 0; }
        table {
            width: 100%;
            border-collapse: collapse;
            font-family: Arial, sans-serif;
        }
        td {
            border: 2px solid black;
            padding: 10px;
            text-align: center;
            
            font-size: 14px;
        }
        .label {
            
            font-weight: bold;
            background-color: #f4a460; 
        }
        .value {
            
        }
        .highlight {
            /* "대표자"와 "업종"의 배경색 */
        }
        th {  }
        .footer { display: flex; justify-content: space-between; border-top: 1px solid #000; padding-top: 10px; }
        .footer div { width: 100%; text-align: center; }
        .vertical-text {
      text-align: center; /* 가운데 정렬 */
         font-weight: bold;
            background-color: #f4a460; 
    }
table {
      border-collapse: collapse;
      border: 2px solid black; /* 외곽 테두리: 진하게 */
    }
/* .bom_body 아래 테이블에만 적용 */
    .bom_body table {
      border-collapse: collapse; /* 테두리 겹치기 */
    }
    .bom_body table th,
    .bom_body table td {
    height: 30px;
      border: 1px solid #ccc; /* 내부 테두리: 연하게 (#ccc는 연한 회색) */
      padding: 10px; /* 셀 내부 여백 */
    }
    /* 외곽 테두리와 내부 테두리 겹침 조정 */
    .bom_body table th:first-child,
    .bom_body table td:first-child {
      border-left: 1px solid #ccc;
    }
    .bom_body table th:last-child,
    .bom_body table td:last-child {
      border-right: 1px solid #ccc;
    }
    .bom_body table tr:first-child th,
    .bom_body table tr:first-child td {
      border-top: 1px solid #ccc;
    }
    .bom_body table tr:last-child th,
    .bom_body table tr:last-child td {
      border-bottom: 1px solid #ccc;
    }

    </style>
</head>
<body>
    <div class="title">&nbsp;&nbsp;발&nbsp;&nbsp;&nbsp;주&nbsp;&nbsp;&nbsp;서&nbsp;&nbsp;</div>
    <div class="info-container">
        
        <div class="info-box" style="max-width:35%">
            <table>
                <tr>
                    <td class="label">견적서</td>
                    <td class="value"  >(주)아이씨엠코리아(I.C.M Korea)</td>
                </tr>
                <tr>
                    <td class="label">발주일자</td>
                    <td class="value" >2025년 5월 3일</td>
                </tr>
                <tr>
                    <td colspan=2></td>
                </tr>
            </table>
            <div class="info-box" style="width: 100%; text-align: left;">
                <h3>아래와 같이 발주합니다</h3>
            </div>
        </div>
        <div class="info-box">
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
        <tbody>
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
                <td></td>
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
st.components.v1.html(html_code, height=1200, scrolling=True)    
