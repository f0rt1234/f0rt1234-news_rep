import streamlit as st
import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import re
import datetime



st.title("Yahooニュースアクセスランキング")
with st.sidebar:
    st.title("ver.01")
    now = datetime.datetime.now()
    st.text(now)
    st.divider()
    st.radio("NEWS",["YAHOO","NHK()"])

# アクセスするURL
url = "https://news.yahoo.co.jp/ranking/access/news"

# URLにアクセスする resに帰ってくる
res = requests.get(url)

# res.textをBeautifulSoupで扱うための処理
soup = BeautifulSoup(res.content, "html.parser")

# href属性に特定の文字が含まれているものを検索
elems = soup.find_all(href=re.compile("news.yahoo.co.jp/articles"))

# 取得した情報の数
num = len(elems)

# リストの内包表記で初期化
#news = [["" for i in range(2)] for j in range(num)]

# numpyライブラリで初期化
news = np.zeros((num,3), dtype='object')

# 保存するときにタイトル行は要れるので、データのみ格納
i = 0
for elem in elems:


    # ハイライト記事の取得
    res_detail = requests.get(elem.attrs['href'])
    soup_detail = BeautifulSoup(res_detail.content, "html.parser")
    elems_detail = soup_detail.find(class_=re.compile("highLightSearchTarget"))

    # データの格納

    news[i][0] = elem.text
    news[i][1] = elem.attrs['href']
    news[i][2] = elems_detail.text
    
    st.write("### News# : " + elem.text)
    st.write("url : " + elem.attrs['href'])
    with st.expander("Read article..."):
    	st.write(elems_detail.text)
    st.divider()

