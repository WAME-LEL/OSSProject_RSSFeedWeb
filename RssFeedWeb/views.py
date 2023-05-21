# Create your views here.

# def index(request):
#     # context = {'question_list': list}
#     return render(request, 'pybo/question_list.html')

# views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
import feedparser
from bs4 import BeautifulSoup

from .forms import SubscribeForm
from .models import subsData

def rss_feed(request):
    # RSS 피드 주소
    # rss_url = "https://computer-science-student.tistory.com/rss"
    rss_url = "https://joel-dev.site/rss"
    # RSS 피드 파싱
    feed = feedparser.parse(rss_url)



    # 최신 글 하나 가져오기
    latest_entry = feed.entries[0]
    second = feed.entries[1]
    third = feed.entries[2]

    entries = []

    for entry in feed.entries:
        # 항목의 내용(content)에서 <p> 태그의 데이터만 추출
        content = entry.description
        soup = BeautifulSoup(content, 'html.parser')
        p_tags = soup.find_all('p')

        paragraphs = []

        # <p> 태그의 데이터를 paragraphs 리스트에 추가
        for p in p_tags:
            if p.string != '\xa0' and p.string is not None:  # &nbsp; 태그 거르기
                paragraphs.append(p.string)

        entries.append({
            'title': entry.title,
            'paragraphs': paragraphs
        })

    context = {
        'entries': entries
    }

    # 템플릿 렌더링
    return render(request, "RssFeedWeb/rss_feed.html", {"feed": feed, "latest_entry": latest_entry, "second": second, "third": third, "paragraphs": paragraphs, "context": context})

#구독 버튼, 돌아오는 버튼 이벤트,구독기능
def sub(request):
    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():

            form.save()
            return redirect('http://localhost:8000/latest/feed/sub/')
    else:
        form = SubscribeForm()

    sub_list = subsData.objects.all()

    return render(request, 'RssFeedWeb/sub.html', {'form': form, 'sub_list': sub_list})
def back(request):
    return render(request,'RssFeedWeb/rss_feed.html')

def detail(request):
    return render(request,'RssFeedWeb/sub.html')
def sublist(request):
    sub_list=subsData.objects.all()
    context={'sub_list':sub_list}
    return render(request,'RssFeedWeb/test.html',context)

def RSS_Del(request,subsData_id):
    subscribe = get_object_or_404(subsData, pk=subsData_id)
    subscribe.delete()
    return render(request, 'RssFeedWeb/sub.html', subsData_id=subsData.id)