# Create your views here.
from django.http import HttpResponse
# views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_protect
from django.utils import timezone
import feedparser
from bs4 import BeautifulSoup

from .forms import SubscribeForm
from .models import subsData
from .forms import ScrapForm
from .models import scrapData
from datetime import datetime, timedelta


def rss_feed(request):
    # RSS 피드 주소


    if subsData.objects.exists():
        today = datetime.now().date()
        try:
            selected_days = int(request.GET.get('days', 0))
        except:
            selected_days = 0



        subs_data = subsData.objects.first()
        urls = subsData.objects.all()
        result = []

        for sub in urls:
            rss_Url = sub.link
            subList = feedparser.parse(rss_Url)
            result.append(subList)

        # RSS 피드 파싱
        feed = result[0]

        # 최신 글 하나 가져오기
        latest_entry = feed.entries[0]
        second = feed.entries[1]
        third = feed.entries[2]

        contextTest = []

        for blog in result:
            entries = []

            i = 0

            for entry in blog.entries:
                published_date = datetime.strptime(entry.published,
                                                   "%a, %d %b %Y %H:%M:%S %z").date() if entry.published else None

                yesterday = today - timedelta(days=selected_days)
                if published_date and yesterday <= published_date <= today:
                    if i >= 3:
                        break
                        # 항목의 내용(content)에서 <p> 태그의 데이터만 추출
                    content = entry.description
                    soup = BeautifulSoup(content, 'html.parser')
                    p_tags = soup.find_all('p')


                    paragraphs = []

                    # <p> 태그의 데이터를 paragraphs 리스트에 추가
                    for p in p_tags:
                        if p.string != '\xa0' and p.string is not None:  # &nbsp; 태그 거르기
                            paragraphs.append(p.string)

                    if not paragraphs:
                        paragraphs.append(content)
                        print(content)

                    if paragraphs[0] == '':
                        newsValue = entry.content[0].value
                        soup = BeautifulSoup(newsValue, 'html.parser')
                        newsSummary = soup.find_all('p')
                        newsSummary = [p.get_text() for p in newsSummary]
                        paragraphs.append(newsSummary[0])

                    entries.append({
                        'title': entry.title,
                        'paragraphs': paragraphs
                    })

                    i = i + 1

            contextTest.append(
                {'entries': entries, 'blog': blog.feed.title, 'first': blog.entries[0], 'second': blog.entries[1],
                 'third': blog.entries[2]})

        # 템플릿 렌더링
        return render(request, "RssFeedWeb/rss_feed.html", {"feed": feed, "url": urls, "result": result, 'contextTest': contextTest, 'selected_days': selected_days})
    else:
        return render(request, "RssFeedWeb/empty.html")


# 구독 버튼, 돌아오는 버튼 이벤트,구독기능
@csrf_protect
def sub(request):
    url = subsData.objects.all()
    result = []
    for sub in url:
        rss_Url = sub.link
        subList = feedparser.parse(rss_Url)
        result.append(subList)

    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()

            # return redirect('https://rss-feed-web.fly.dev/sub/')    #배포 서버용
            return redirect('http://localhost:8000/sub/')  # 로컬 호스트용
        else:
            print(form.errors)  # 폼 에러 출력
    else:
        form = SubscribeForm()

    sub_list = subsData.objects.all()
    return render(request, 'RssFeedWeb/sub.html', {'form': form, 'sub_list': sub_list, "result": result, "url": url})


def back(request):
    return render(request, 'RssFeedWeb/rss_feed.html')


def detail(request):
    return render(request, 'RssFeedWeb/sub.html')


def sublist(request):
    sub_list = subsData.objects.all()
    context = {'sub_list': sub_list}
    return render(request, 'RssFeedWeb/test.html', context)


def RSS_Del(request, subsData_id):
    # 구독 취소 기능
    subscribe = get_object_or_404(subsData, pk=subsData_id)
    subscribe.delete()
    # return render(request, 'RssFeedWeb/sub.html', {'subsData_id':subsData.id})
    previous_url = request.META.get('HTTP_REFERER', '/')
    return redirect(previous_url)


def Sub_cate(request, ob_id):
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
    four = feed.entries[3]
    five = feed.entries[4]

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
        if not paragraphs:
            paragraphs.append(content)
            print(content)

        if paragraphs and paragraphs[0] == '':
            newsValue = entry.content[0].value
            soup = BeautifulSoup(newsValue, 'html.parser')
            newsSummary = soup.find_all('p')
            newsSummary = [p.get_text() for p in newsSummary]
            if newsSummary:
                paragraphs.append(newsSummary[0])

        entries.append({
            'title': entry.title,
            'paragraphs': paragraphs
        })

    context = {
        'entries': entries
    }

    # 템플릿 렌더링
    return render(request, "RssFeedWeb/category.html",
                  {"feed": feed, "latest_entry": latest_entry, "second": second, "third": third, "four":four, "five":five,
                   "paragraphs": paragraphs, "context": context, "url": url, "result": result})


def scrap(request):
    url = subsData.objects.all()
    scrap=scrapData.objects.all()
    result = []
    for sub in url:
        rss_Url = sub.link
        subList = feedparser.parse(rss_Url)
        result.append(subList)



    return render(request, "RssFeedWeb/scrap.html",
           {"result":result,"url":url})

def scrap_Del(request, scrapData_id):
    # 구독 취소 기능
    scrap = get_object_or_404(scrapData, pk=scrapData_id)
    scrap.delete()
    # return render(request, 'RssFeedWeb/sub.html', {'subsData_id':subsData.id})
    previous_url = request.META.get('HTTP_REFERER', '/')
    return redirect(previous_url)

def scrapSave(request):
    if request.method == 'POST':
        form = ScrapForm(request.POST)
        if form.is_valid():
            link = form.cleaned_data['link']
            title = form.cleaned_data['title']

            # scrapData 모델에 저장
            scrap = scrapData(link=link, title=title)
            scrap.save()

            return HttpResponse('저장 완료')
    else:
        form = ScrapForm()

    context = {'form': form}
    return render(request, "RssFeedWeb/scrap.html", context)