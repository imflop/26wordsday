from django.urls import path

from words.views import WordListView, WordDetail

app_name = 'words'

urlpatterns = [
    path('list/', WordListView.as_view(), name='words-list'),
    path('word/<slug:slug>/<int:word_id>', WordDetail.as_view(), name='word-detail')
]
