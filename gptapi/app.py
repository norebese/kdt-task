import streamlit as st
import requests
from pymongo import MongoClient
import pandas as pd
import time

mongo_url = 'mongodb+srv://c01039520824:VJlhIYbNW68HgIXu@cluster0.beqs9le.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'

client = MongoClient(mongo_url) # 응답 확인
database = client['aiproject'] # 데이터베이스 선택
collection = database['adinfo'] # 컬렉션 선택

st.title('광고 문구 서비스앱')
generate_ad_url = 'http://127.0.0.1:8000/create_ad'

product_name = st.text_input('제품 이름')
details = st.text_input('주요 내용')
options = st.multiselect('광고 문구의 느낌', options=['기본', '재밌게', '차분하게', '과장스럽게', '참신하게', '고급스럽게'], default=['기본'])

ad_data = list(collection.find({}))
df = pd.DataFrame(ad_data)
columns_to_display = ['product_name', 'details', 'ad']

if st.button("광고 문구 생성하기"):
    try:
        response = requests.post(
            generate_ad_url,
            json={"product_name": product_name,
                "details": details,
                "tone_and_manner": ", ".join(options)})
        ad = response.json()['ad']
        st.success(ad)
        data_insert = {'product_name': product_name, 'details': details, 'ad': ad}
        result = collection.insert_one(data_insert)
        ad_data = list(collection.find({}))
        df = pd.DataFrame(ad_data)
        st.write(df[columns_to_display])
    except:
        st.error("연결 실패!")
