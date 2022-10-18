from django.urls import path, reverse_lazy
from django.views.generic import TemplateView, RedirectView

from . import views

urlpatterns = [
    # path('', TemplateView.as_view(template_name='news/cs.html')),
    path('', RedirectView.as_view(url=reverse_lazy('home'))),
    path('news/', views.home, name='home'),
    path('news/<int:link>/', views.article, name='article'),
    path('news/create/', views.CreateNewsView.as_view(), name='create')
]
