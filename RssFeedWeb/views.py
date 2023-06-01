# Create your views here.

# views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_protect
from django.utils import timezone
import feedparser
from bs4 import BeautifulSoup


from .forms import SubscribeForm
from .models import subsData


def rss_feed(request):
    # RSS 피드 주소
    subs_data = subsData.objects.first()
    url = subsData.objects.all()
    result=[]
    for sub in url:
        rss_Url = sub.link
        subList = feedparser.parse(rss_Url)
        result.append(subList)

    rss_url = subs_data.link
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
    return render(request, "RssFeedWeb/rss_feed.html",
                  {"feed": feed, "latest_entry": latest_entry, "second": second, "third": third,
                   "paragraphs": paragraphs, "context": context, "url": url,"result":result})


# 구독 버튼, 돌아오는 버튼 이벤트,구독기능
@csrf_protect
def sub(request):
    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():
            form.save()
            # return redirect('https://rss-feed-web.fly.dev/sub/')    #배포 서버용
            return redirect('http://localhost:8000/sub/')        #로컬 호스트용

    else:
        form = SubscribeForm()

    sub_list = subsData.objects.all()
    return render(request, 'RssFeedWeb/sub.html', {'form': form, 'sub_list': sub_list})


def back(request):
    return render(request, 'RssFeedWeb/rss_feed.html')



def detail(request):
    return render(request, 'RssFeedWeb/sub.html')

def sublist(request):
    sub_list = subsData.objects.all()
    context = {'sub_list': sub_list}
    return render(request, 'RssFeedWeb/test.html', context)


def RSS_Del(request, subsData_id):
#구독 취소 기능
    subscribe = get_object_or_404(subsData, pk=subsData_id)
    subscribe.delete()
    # return render(request, 'RssFeedWeb/sub.html', {'subsData_id':subsData.id})
    previous_url = request.META.get('HTTP_REFERER', '/')
    return redirect(previous_url)

def Sub_cate(request,ob_id):
    url = subsData.objects.all()
    subscribe = get_object_or_404(subsData, pk=ob_id)
    rss_url = subscribe.link
    result = []
    # RSS 피드 파싱
    feed = feedparser.parse(rss_url)
    for sub in url:
        rss_Url = sub.link
        subList = feedparser.parse(rss_Url)
        result.append(subList)


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
    return render(request, "RssFeedWeb/category.html",
                  {"feed": feed, "latest_entry": latest_entry, "second": second, "third": third,
                   "paragraphs": paragraphs, "context": context,"url": url,"result":result})
