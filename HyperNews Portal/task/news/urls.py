from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('news/<link>', views.article, name='article'),
]
