import streamlit as st
import pandas as pd
from menu import menu_with_redirect
# import airtable
from pyairtable import Api
from openai import OpenAI
import json
import copy
# Redirect to app.py if not logged in, otherwise show the navigation menu
st.set_page_config(layout="wide", page_title='자재 발주 시스템(smartMR)')
menu_with_redirect()



api_key = 'patqEfN06y9QLUoS0.0ff77915af3ff09a6aea08f2b64da60016c567129cea7448c8d903265d5cda71'

base_id= 'appESzks3l70ngxgd'
cosmax_table = 'tbloZpZ5QZY6nZPD0'
component_table = 'tbl8uwQUhuWQMlJtf'
product_table= 'tblreG6m3bTRYMeLy'

#1. 제품 정보
@st.cache_data(ttl=1200)  
def get_product_table_list():
    api = Api(api_key)
    table = api.table(base_id, product_table)
    data = pd.DataFrame(r['fields'] for r in table.all())
    return data


def get_product_list(product_name =None, product_code=None):
    data = get_product_table_list()
    query = ''
    
    if product_name != '' and  product_name is not None:
        query += f'제품코드.str.contains("{product_name}" , case=False, na=False)'
    if product_code != '' and product_code is not None :
        if query != '':
            query+= ' & '
        query += f'제품코드 == "{product_code}"'
    
    return data.query(query)


#2. 자재 정보
@st.cache_data(ttl=1200)  
def get_component_table_list():
    api = Api(api_key)
    table = api.table(base_id, component_table)
    data = pd.DataFrame(r['fields'] for r in table.all())
    return data


def get_component_list(component_name =None, component_code=None , component_maker=None):
    data = get_component_table_list()
    query = ''
    
    if component_name != '' and  component_name is not None:
        query += f'자재명.str.contains("{component_name}" , case=False, na=False)'
    if component_code != '' and component_code is not None :
        if query != '':
            query+= ' & '
        query += f'자재코드 == "{component_code}"'

    if component_maker != '' and component_maker is not None :
        if query != '':
            query+= ' & '
        query += f'업체코드.str.contains("{component_maker}" , case=False, na=False)'
    print(query)
    return data.query(query)



### llm 정보
llm_key = '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'
client = OpenAI(api_key=llm_key , base_url = 'https://api.groq.com/openai/v1')

system_prompt ='''당신은 친절한 AI assistant 입니다.
주어진 정보를 활용하거나, tool 을 활용하여 사용자의 질문에 대답해주세요.
답변은 한국어로만 해주세요. 사용자가 한국인입니다.
'''


tools = [
    {
        "type": "function",
        "function": {
            "name": "get_product_list",
            "description": '''세르쟌느(cherejeanne) 의 상품,제품 리스트를 조회합니다.''',
            "parameters": {
                "type": "object",
                "properties": {
                    "product_name": {"type": "string", "description": "제품명 ( ex. 퐁드땅 루미에르 도레 쿠션 ). 제품의 이름"},
                    "product_code": {"type": "string", "description": "제품 코드( ex. 9CPS0000610 ) 코드 정보"}
                },
                "required": ["product_name", "product_code"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_component_list",
            "description": '''세르쟌느(cherejeanne) 의 자재(부품) 리스트를 조회합니다.''',
            "parameters": {
                "type": "object",
                "properties": {
                    "component_name": {"type": "string", "description": "자재명 ( ex. 쿠퍼스테이션셰르잔느퐁드땅루미에르도레쿠션 ). 자재의 이름"},
                    "component_code": {"type": "string", "description": "자재 코드( ex. 7CPS000041N00 ) 자재 정보"},
                    "component_maker": {"type": "string", "description": "업체명 ( ex. 두보산업 ) 자재를 만드는 업체이름, 업체 정보, vendoer, maker 정보"},
                },
                "required": ["component_name", "component_code" , "component_maker"]
            }
        }
    }



]


def add_numbers(a, b):
    return a + b
  

def get_openai_stream(prompt):
    response_chunks = []
    messages = st.session_state.messages[:]
    messages.insert(0 , {"role": "system", "content": system_prompt})
    
    try:
        stream = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=messages,
            stream=True,
            tools=tools,
            tool_choice="auto"
        )
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                content = chunk.choices[0].delta.content
                response_chunks.append(content)
                yield content
            elif chunk.choices[0].delta.tool_calls:
                info = None
                # Tool 호출 처리
                tool_call = chunk.choices[0].delta.tool_calls[0]
                if tool_call.function.name == "get_product_list":
                    args = json.loads(tool_call.function.arguments)
                    info = get_product_list(args["product_name"], args["product_code"])
                

                if tool_call.function.name == "get_component_list":
                    args = json.loads(tool_call.function.arguments)
                    info = get_component_list(args["component_name"], args["component_code"] , args["component_maker"])

                if info is not None:
                    
                    messages = st.session_state.messages[:]
                    messages.insert(0 , {"role": "system", "content": system_prompt})

                    temp = messages.pop()
                    _temp = copy.deepcopy(temp)
                    _temp['content'] = f'###context:\n {info}\n\n###query: {temp["content"]}' 
                    messages.append(_temp)
                    
                    try:
                        stream = client.chat.completions.create(
                            model="gemma2-9b-it",
                            # model="mistral-saba-24b",
                            messages= messages, 
                            stream=True
                        )
                        for chunk in stream:
                            if chunk.choices[0].delta.content is not None:
                                content = chunk.choices[0].delta.content
                                response_chunks.append(content)
                                
                                yield content
                    except Exception as e:
                        error_msg = f"Error: {str(e)}"
                        print(error_msg)
                        response_chunks.append(error_msg)
                        yield error_msg
                    # 스트리밍 완료 후 전체 응답 저장
                    st.session_state.messages.append({"role": "assistant", "content": "".join(response_chunks)})




    except Exception as e:
        error_msg = f"Error: {str(e)}"
        response_chunks.append(error_msg)
        yield error_msg

# left, right = st.columns((10, 20))

st.title("💬 Chat with AI")
st.info("🚀 cherejeanne 재고 관리 등 업무 관련 문의사항을 AI 에게 문의해보세요.")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "어떻게 도와드릴까요?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    with st.chat_message("assistant"):
        st.write_stream(get_openai_stream(prompt))