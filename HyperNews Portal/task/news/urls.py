from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='news/cs.html')),
    path('news/', views.home, name='home'),
    path('news/<int:link>/', views.article, name='article'),
    path('news/create/', views.CreateNewsView.as_view(), name='create')
]
