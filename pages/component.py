import streamlit as st
import pandas as pd
from menu import menu_with_redirect
from pyairtable import Api
# Redirect to app.py if not logged in, otherwise show the navigation menu
st.set_page_config(layout="wide")
menu_with_redirect()



api_key = 'patqEfN06y9QLUoS0.0ff77915af3ff09a6aea08f2b64da60016c567129cea7448c8d903265d5cda71'


def get_component_list():
    api = Api(api_key)
    table = api.table('appESzks3l70ngxgd', 'tbl8uwQUhuWQMlJtf')
    return table.all()

# at = airtable.Airtable('appESzks3l70ngxgd', api_key)
component_list = get_component_list()


# left, right = st.columns((10, 20))
st.title("자재정보")


data = pd.DataFrame(r['fields'] for r in component_list)
st.dataframe(data , height=1000)



