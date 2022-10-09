from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, Http404
from json import load


def home(request):
    return render(request, 'news/index.html')


def article(request, link):
    with open(settings.NEWS_JSON_PATH, "r") as json_file:
        articles = load(json_file)
    article_to_display = None
    for article in articles:
        if article.get("link", None) == int(link):
            article_to_display = article
    if article_to_display is None:
        raise Http404
    context = {"news": article_to_display}
    return render(request, 'news/article.html', context=context)