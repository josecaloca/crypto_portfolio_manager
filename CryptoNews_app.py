from newscatcherapi import NewsCatcherApiClient
import streamlit as st
from tqdm import tqdm

# URL sources of Crypto news websites
sources = ["coindesk.com", "cointelegraph.com", "bitcoin.com", 
           "cryptopotato.com", "zycrypto.com", "nulltx.com", "coinquora.com",
           "ambcrypto.com", "cryptoslate.com", "crypto.news"]


API_KEY = 'Please input your private api_key' # get api_key from https://newscatcherapi.com/
newscatcherapi = NewsCatcherApiClient(x_api_key=API_KEY)

st.title('🔎 Crypto News Finder')
search_option = st.sidebar.radio('🔎 Crypto News Finder', options=['Top Headlines', 'Search Keyword'])


# Streamlit app configuration
def add_articles(articles):
  columns = st.columns(2)
  no_of_articles = len(articles)
  article_index = 0
  col_index = -1
  while True:
    article = articles[article_index]
    with columns[0 if col_index < 0 else 1]:
      title = article["title"]
      # print(title)
      link = article["link"]
      date = article["pub_date"]
      st.markdown(f"### [{title}]({link})")
      if article["image"] == None:
        if "nulltx" in link:
          st.image("https://nulltx.com/wp-content/uploads/2018/10/nulltx-logo-red.png")
        if "cryptoslate" in link:
          st.image("https://cryptoslate.com/wp-content/themes/cryptoslate-2020/images/cs-media-logo-dark.png")
      else:
        st.image(article["image"])
      st.caption(f"{date}")
      st.write(article["summary"])
    
    if no_of_articles == article_index + 1:
        return
      
    article_index += 1
    col_index *= -1


def article_gather(articles_filter):
    for article in news_articles["articles"]:
        temp_article = {}
        temp_article["title"] = article["title"]
        temp_article["link"] = article["link"]
        temp_article["pub_date"] = article["published_date"]
        temp_article["summary"] = article["excerpt"]
        temp_article["image"] = article["media"]
        articles_filter.append(temp_article)


api_articles = []
keyword_articles = []

if search_option == 'Top Headlines':
    news_articles = newscatcherapi.get_search(q='*', sources = sources, from_ = "16/04/2022")
    article_gather(api_articles)

    add_articles(api_articles)

elif search_option == 'Search Keyword':
    search_keyword = st.sidebar.text_input('Enter Search Keyword:')

    if not search_keyword:
        st.write('Please enter a search keyword')

    else:
        while True:
            try:
                news_articles = newscatcherapi.get_search(q=search_keyword, sources = sources, from_ = "16/04/2022")
                article_gather(keyword_articles)
                add_articles(keyword_articles)
                break
            except:
                st.write('Please enter new search keyword. There is no Crypto News existing with this keyword.')
                break
         
