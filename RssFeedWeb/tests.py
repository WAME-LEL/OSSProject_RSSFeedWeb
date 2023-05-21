from django.test import TestCase

# Create your tests here.

from .models import subsData

def rss_feed(request):
    subs_data = subsData.objects.first()
    rss_url = subs_data.link
    print(subs_data)
