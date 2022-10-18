from django.shortcuts import render
from django.conf import settings
from django.http import Http404
from itertools import groupby
from json import load


def simple_date(long_date_string):
    return long_date_string[:10]

def home(request):
    with open(settings.NEWS_JSON_PATH, "r") as json_file:
        articles = load(json_file)
    articles.sort(key=lambda item: item['created'], reverse=True)

    # items = []
    # created = articles[0]['created'][:10]
    # item = {'date': created, 'news': []}
    #
    # for article in articles:
    #     if article['created'][:10] == created[:10]:
    #         item['news'].append(article)
    #     else:
    #         items.append(item)
    #         created = article['created'][:10]
    #         item = {'date': created, 'news': [article]}
    # items.append(item)

    items = [{'date': date, 'news': list(news)} for date, news in
                groupby(articles, lambda x: simple_date(x['created']))]


    context = {'items': items}
    return render(request, 'news/index.html', context=context)


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
