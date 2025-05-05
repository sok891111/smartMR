import streamlit as st
import pandas as pd
from menu import menu_with_redirect
# import airtable
from pyairtable import Api
# Redirect to app.py if not logged in, otherwise show the navigation menu
st.set_page_config(layout="wide", page_title='자재 발주 시스템(smartMR)')
menu_with_redirect()



api_key = 'patqEfN06y9QLUoS0.0ff77915af3ff09a6aea08f2b64da60016c567129cea7448c8d903265d5cda71'




def get_product_list():
    api = Api(api_key)
    table = api.table('appESzks3l70ngxgd', 'tblreG6m3bTRYMeLy')
    return table.all()

product_list = get_product_list()


# left, right = st.columns((10, 20))
st.title("제품정보")


data = pd.DataFrame(r['fields'] for r in product_list)
st.dataframe(data , height=1000)



