# Create your views here.
# from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import requests
from bs4 import BeautifulSoup

from wordcloud import WordCloud, STOPWORDS
from konlpy.tag import Okt
from collections import Counter
import matplotlib.pyplot as plt

f = open('url.txt', 'w')
page_counter = 1
url_count = 0

for i in range(1, 6):
    html = requests.get(f'http://www.dailypop.kr/news/articleList.html?page={i}&total=168&sc_section_code'
                        '=&sc_sub_section_code=&sc_serial_code=&sc_area=A&sc_level=&sc_article_type=&sc_view_level'
                        '=&sc_sdate=&sc_edate=&sc_serial_number=&sc_word=%EC%A7%91%EC%BD%95')
    soup = BeautifulSoup(html.content, 'html.parser')
    url_list = soup.find(class_='article-list-content text-left').find_all('a')

    for link in url_list:
        if url_count == 99:
            f.write('http://www.dailypop.kr/'+link.get('href'))
        else:
            f.write('http://www.dailypop.kr/' + link.get('href')+'\n')
        url_count += 1
f.close()

# res = requests.get('http://www.dailypop.kr/news/articleView.html?idxno=47220')
# soup = BeautifulSoup(res.content, 'html.parser')

# title = soup.find('title')
# body = soup.find(id='article-view-content-div').find_all('p')
# images = soup.find(id='article-view-content-div').find_all('img')
# imgs = []
# for i, image in enumerate(images):
#     # print('http://www.dailypop.kr'+image.get('src'))
#     if(i!=6):
#         imgs.append('http://www.dailypop.kr'+image.get('src'))
#
# content = []
# stringTypeContent = ''
# for i, e in enumerate(body):
#     content.append(e.get_text())
#     stringTypeContent += e.get_text()

# wc = WordCloud(font_path='/Library/Fonts/HMKMMAG.TTF', background_color='white', width=500, height=500, max_words=20, max_font_size=100)
# okt = Okt()
# noun = okt.nouns(stringTypeContent)
# count = Counter(noun)
#
# noun_list = count.most_common()
# # for v in noun_list
#     # print(v)
#
# # print(dict(noun_list))
# # wc = wc.generate(stringTypeContent)
# wc.generate_from_frequencies(dict(noun_list))
# wc.to_file('./wc.png')
# plt.figure(figsize=(10, 8))
# plt.imshow(wc)
# plt.axis('off')
# plt.show()

def index(request):
    # return HttpResponse('검색하실 url을 입력해주세요.')
    template = loader.get_template('news/index.html')

    context = {
        'title': title.get_text(),
        'body': content,
        'images': imgs
    }
    return HttpResponse(template.render(context, request))


# def detail(request, news_id):
#     return HttpVResponse(body, news_id)
