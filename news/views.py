from django.http import HttpResponse
from django.template import loader

import requests
from bs4 import BeautifulSoup

from wordcloud import WordCloud, STOPWORDS
from konlpy.tag import Okt
from collections import Counter
import matplotlib.pyplot as plt

# url_list, 텍스트 파일 생성(쓰기) 및 url_list 100개 저장
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
            f.write(f'http://www.dailypop.kr/'+link.get('href')+'\n')
        url_count += 1
f.close()

# url_list read, 텍스트 파일 읽기 및 각 기사(url)의 내용들을 한 변수에 저장
stringTypeContent = ''
with open('url.txt', 'r') as file:
    for line in file:
        line = line.strip('\n')
        html = requests.get(line)
        soup = BeautifulSoup(html.content, 'html.parser')
        body = soup.find(id='article-view-content-div').find_all('p')
        spwords = set(STOPWORDS)
        for i, e in enumerate(body):
            stringTypeContent += e.get_text()
file.close()

# 워드클라우드 설정 및 키워드 빈도별로 분류
wc = WordCloud(font_path='/Library/Fonts/HMKMMAG.TTF', background_color='white',
               width=500, height=500, max_words=20, max_font_size=100, stopwords=spwords)
okt = Okt()
noun = okt.nouns(stringTypeContent)
count = Counter(noun)
noun_list = count.most_common()

# stopwords 키워드 제거(워드클라우드 분석에 도움안되는 한 글자의 키워드들 제거)
temp = []
for i, noun in enumerate(dict(noun_list)):
    if noun == '이' or noun == '위' or noun == '를' or noun == '등' or noun == '것' or noun == '로' or noun == '수':
        temp.append(noun_list[i])
for i, e in enumerate(temp):
    noun_list.remove(temp[i])

# 워드 클라우드 생성
wc.generate_from_frequencies(dict(noun_list))
wc.to_file('./wc.png')
plt.figure(figsize=(10, 8))
plt.imshow(wc)
plt.axis('off')
plt.show()
print('success')


def index(request):
    template = loader.get_template('news/index.html')

    return HttpResponse(template.render('exit', request))
