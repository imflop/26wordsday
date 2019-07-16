from django.urls import path

from words.views import WordListView, WordDetail

urlpatterns = [
    path('', WordListView.as_view(), name='words-list'),
    path('word/<slug:slug>/<int:word_id>', WordDetail.as_view(), name='word-detail')
]
