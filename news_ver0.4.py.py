import requests
from bs4 import BeautifulSoup
import re
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time


def main():
    status_text = st.empty()

    # プログレスバー
    progress_bar = st.progress(0)

    for i in range(100):
        status_text.text(f'Progress: {i}%')

        # for ループ内でプログレスバーの状態を更新する
        progress_bar.progress(i + 1)
        time.sleep(0.05)

    # 処理が完了したら空のコンポーネントで上書き
    status_text.empty()
    progress_bar.empty()

# カテゴリ用の空の辞書を作成
category_dict = {'category': [], 'news#': []}

st.title("news_APP")
tab1, tab2, tab3, tab4  = st.tabs(["News", "DataFrame", "Bar Plot", "About App"])

with tab1:
   st.header("News") 
   
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
   
       # ハイライト記事の取得
       res_detail = requests.get(data.attrs['href'])
       soup_detail = BeautifulSoup(res_detail.content, "html.parser")
       elems_detail = soup_detail.find(class_=re.compile("highLightSearchTarget")) 
       
       # ハイライト記事のカテゴリを取得        
       category_value  = soup_detail.find('li', class_='sc-fKFxtB gDMWVt').a['href'].split('/')[-1]
       
       # カテゴリ用の要素の追加
       category_dict['category'].append(category_value)
       category_dict['news#'].append(name.contents[0])
       
   
       # ヤフーニュースの見出しとカテゴリ,URLの情報を出力する
       st.divider()
       st.write(f"News#{i} : {category_value }")
       st.write(f"{name.contents[0]}")
       st.write(data.attrs["href"])


       
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
       
       

              
with tab2:

   if __name__ == '__main__':
    main()
   st.header("DataFrame") 
   st.divider()
   
   # データフレーム作成
   df = pd.DataFrame(category_dict)
   
   # インデックスを1から始める
   df.index = df.index + 1
    
   st.write(df)


with tab3:
   if __name__ == '__main__':
    main()
   st.header("Bar Plot") 
   st.divider() 

   # categoryごとの個数を集計
   category_counts = df['category'].value_counts()
  
   # カラーマップの範囲を指定
   cmap = plt.cm.get_cmap('viridis', len(category_counts))
   
   # 要素の数だけ色を準備
   colors = [cmap(i) for i in range(len(category_counts))]
   
   # 棒グラフで表示
   fig, ax = plt.subplots()

   # カテゴリごとの個数を降順にソートしてから棒グラフを描画
   category_counts.sort_values(ascending=False).plot(kind='bar', color=colors, ax=ax)
   
   ax.set_yticks(np.arange(0, 41, 2))
   ax.set_xlabel('category')
   ax.set_ylabel('count')
   
   # MatplotlibのグラフをStreamlitで表示
   st.pyplot(fig)

   
with tab4:
   if __name__ == '__main__':
    main()
   app_information = """

	アプリ名: news_APP
	
	目的:
	このアプリケーションは、ヤフーニュースのトップページからニュース記事を抽出し、ユーザーに見出し、URL、カテゴリごとの画像を提供します。またユーザーは簡単に世間の関心のあるカテゴリを知ることができます。

	技術的な要素:

	スクレイピング: BeautifulSoupライブラリを使用してヤフーニュースのトップページからデータを収集します。
	ユーザーインターフェース: Streamlitを使用して、使いやすく直感的なUIを提供します。
	データ分析: 収集したデータからPandasデータフレームを作成し、カテゴリごとの統計を表示します。
	データの可視化: Matplotlibを使用して、カテゴリごとの記事数を示すBar Plotを作成します。

	デザインの注意:

	タブの使用: タブを活用して、異なるセクションへのアクセスを簡単にしました。
	エキスパンダーの活用: ユーザーが記事の詳細情報や画像を閲覧できるように、エキスパンダーを導入しました。
	
	苦労したポイント:
	
	スクレイピングしたURLから必要なデータを抽出する作業でした。
	
	改善の余地:

	より多くのデータソース: 他のニュースサイトからも情報を収集できるように拡張する。
	ページの読み込み時間を短縮し、ロード時間を短くする工夫。
        """
        
   app_difference = """   
	Copyright-Free news_APP(著作権対策用 )と DataFrame との差異:
	news_APP:
	- 見出しあり
	- 写真あり
	- 記事の内容が含まれている

	Copyright-Free news_APP(著作権対策用 ):
	- 見出しなし
	- 写真なし
	- 記事の内容なし
	- 記事の文字数をカウントする機能あり

	DataFrame:
	- 記事の見出しなし
	- 記事の文字数あり

	"""
   st.write(app_information)
   st.divider()
   st.write(app_difference)
   # 一番下に表示する文字列
st.divider()
st.markdown("<div style='text-align: center;'>© 2024 F</div>", unsafe_allow_html=True)
   
  
