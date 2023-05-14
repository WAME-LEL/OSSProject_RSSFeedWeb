from django.shortcuts import render
from django.contrib.syndication.views import Feed
from django.urls import reverse

# Create your views here.
from django.http import HttpResponse

# def index(request):
#     # context = {'question_list': list}
#     return render(request, 'pybo/question_list.html')

# views.py

from django.shortcuts import render
import feedparser
from bs4 import BeautifulSoup
import requests

def rss_feed(request):
    # RSS 피드 주소
    rss_url = "https://computer-science-student.tistory.com/rss"

    # RSS 피드 파싱
    feed = feedparser.parse(rss_url)

    # HTML 파싱
    # res = requests.get(feed.entries[0].description)
    # soup = BeautifulSoup(res.text, "html.parser")

    # 원하는 정보 가져오기
    # title = soup.select_one('pre id="code_1651423605149"').text

    # 최신 글 하나 가져오기
    latest_entry = feed.entries[0]

    # 템플릿 렌더링
    return render(request, "RssFeedWeb/rss_feed.html", {"feed": feed, "latest_entry": latest_entry})