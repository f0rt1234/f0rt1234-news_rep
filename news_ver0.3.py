

import requests
from bs4 import BeautifulSoup
import re
import streamlit as st


st.title("アクセス上位から世間の関心を知ろう")
tab1, tab2, tab3 = st.tabs(["Yahoo", "NHK", "graph"])

with tab1:
   # ヤフーニュースのトップページ情報を取得する
   URL = "https://news.yahoo.co.jp/ranking/access/news"
   rest = requests.get(URL)

   # BeautifulSoupにヤフーニュースのページ内容を読み込ませる
   soup = BeautifulSoup(rest.content, "html.parser")

   # ヤフーニュースの見出しとURLの情報を取得
   data_list = soup.find_all(href=re.compile("news.yahoo.co.jp/articles"))
   name_list = soup.find_all("div", class_="newsFeed_item_title")

   # ヤフーニュースの見出しとURLの情報を出力する
   for i, (data, name) in enumerate(zip(data_list, name_list), start=1):
       st.write(f"News#{i} : {name.contents[0]}")
       st.write(data.attrs["href"])



       # ハイライト記事の取得
       res_detail = requests.get(data.attrs['href'])
       soup_detail = BeautifulSoup(res_detail.content, "html.parser")
       elems_detail = soup_detail.find(class_=re.compile("highLightSearchTarget"))   
       
       # ハイライト記事のimg取得
       img_tags = soup_detail.find_all(srcset=re.compile("newsatcl-pctr.c.yimg.jp/t/amd-img.*&fmt=webp"))
    

    
       
       
       


       with st.expander("Read article..."): 
       
            for img_tag in img_tags:   
               # 正規表現を使用してsrcset属性の値を取得
               # .jpg 以下を取り除く
               match = re.search(r'(https://.+?\.jpg)', img_tag['srcset'])
               if match:
                   image_url = match.group(1)
                # imageを出力する
                
                   st.image(image_url, width=200)
               else:
                   st.write("URLが見つかりませんでした。")        
            # ハイライト記事を出力する
       	    st.write(elems_detail.text)
       st.divider()
       
             
           
              
with tab2:
   st.header("NHK")
   st.image("https://static.streamlit.io/examples/dog.jpg", width=200)

with tab3:
   st.header("GRAPF")
   st.image("https://static.streamlit.io/examples/owl.jpg", width=200)


