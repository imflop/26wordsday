from django.urls import path
from words.views import WordListView


urlpatterns = [
    path('', WordListView.as_view(), name='words-list')
]
