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

# f = open('url.txt', 'w')
# page_counter = 1
# url_count = 0
#
# for i in range(1, 6):
#     html = requests.get(f'http://www.dailypop.kr/news/articleList.html?page={i}&total=168&sc_section_code'
#                         '=&sc_sub_section_code=&sc_serial_code=&sc_area=A&sc_level=&sc_article_type=&sc_view_level'
#                         '=&sc_sdate=&sc_edate=&sc_serial_number=&sc_word=%EC%A7%91%EC%BD%95')
#     soup = BeautifulSoup(html.content, 'html.parser')
#     url_list = soup.find(class_='article-list-content text-left').find_all('a')
#
#     for link in url_list:
#         if url_count == 99:
#             f.write('http://www.dailypop.kr/'+link.get('href'))
#         else:
#             f.write('http://www.dailypop.kr/' + link.get('href')+'\n')
#         url_count += 1
# f.close()
#
# for i in range(100):
#     print(i)

res = requests.get('http://www.dailypop.kr/news/articleView.html?idxno=47336')
soup = BeautifulSoup(res.content, 'html.parser')

body = soup.find(id='article-view-content-div').find_all('p')
spwords = set(STOPWORDS)
spwords.add('약')
spwords.add('등')
content = []
stringTypeContent = ''
for i, e in enumerate(body):
    content.append(e.get_text())
    stringTypeContent += e.get_text()
wc = WordCloud(font_path='/Library/Fonts/HMKMMAG.TTF', background_color='white',
               width=500, height=500, max_words=20, max_font_size=100, stopwords=spwords)
okt = Okt()
noun = okt.nouns(stringTypeContent)
count = Counter(noun)

noun_list = count.most_common()
temp = []
# print(noun_list)
for i, noun in enumerate(dict(noun_list)):
    if noun == '약' or noun == '수' or noun == '것' or noun == '위' or noun == '로' or noun == '등' or noun == '개':
        temp.append(noun_list[i])
        # noun_list.remove(noun_list[i])

for i, e in enumerate(temp):
    noun_list.remove(temp[i])

# wc = wc.generate(stringTypeContent)
wc.generate_from_frequencies(dict(noun_list))
wc.to_file('./wc.png')
plt.figure(figsize=(10, 8))
plt.imshow(wc)
plt.axis('off')
plt.show()


def index(request):
    # return HttpResponse('검색하실 url을 입력해주세요.')
    template = loader.get_template('news/index.html')

    return HttpResponse(template.render('a', request))

# def detail(request, news_id):
#     return HttpVResponse(body, news_id)
