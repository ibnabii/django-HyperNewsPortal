from django.forms import ModelForm

from .models import News

class ArticleForm(ModelForm):
    class Meta:
        model = News
        fields = ['title', 'text']