from itertools import groupby
from json import load, dumps
from datetime import datetime

from django.conf import settings
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from .forms import ArticleForm


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
    q = request.GET.get('q', '')
    if q:
        articles = filter(lambda x: q.lower() in x['title'].lower(), articles)
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


def get_link(articles):
    return max([int(x['link']) for x in articles]) + 1


class CreateNewsView(FormView):
    form_class = ArticleForm
    template_name = 'news/news_form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        with open(settings.NEWS_JSON_PATH, "r") as json_file:
            articles = load(json_file)
        articles.append(
            {
                'title': form.cleaned_data.get('title'),
                'text': form.cleaned_data.get('text'),
                'created': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'link': get_link(articles)
            }
        )
        with open(settings.NEWS_JSON_PATH, 'w') as json_file:
            json_file.write(dumps(articles, indent=4))
        return redirect(reverse_lazy('home'))
