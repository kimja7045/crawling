from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
import requests
from bs4 import BeautifulSoup

res = requests.get('http://www.dailypop.kr/news/articleView.html?idxno=47220')
soup = BeautifulSoup(res.content, 'html.parser')

title = soup.find('title')
body = soup.find(id='article-view-content-div').find_all('p')
# body = soup.find(id='article_body')
# body = soup.find(class_='ab_subtitle').find_all('h2')
images = soup.find(id='article-view-content-div').find_all('img')

imgs = []
for i, image in enumerate(images):
    # print('http://www.dailypop.kr'+image.get('src'))
    if(i!=6):
        imgs.append('http://www.dailypop.kr'+image.get('src'))


content = []
for i, e in enumerate(body):
    content.append(e.get_text())

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