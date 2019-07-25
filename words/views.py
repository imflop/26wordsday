from django.core.cache import cache
from django.views.generic import ListView, DetailView

from utils.utils import get_key_from_datetime_now
from .models import Word


class WordListView(ListView):
    model = Word
    template_name = 'words_list.html'
    context_object_name = 'words_list'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        words = cache.get(get_key_from_datetime_now())
        context.update({
            'words': words
        })
        return context


class WordDetail(DetailView):
    model = Word
    template_name = 'word.html'
    pk_url_kwarg = 'word_id'
    slug_url_kwarg = 'slug'
    query_pk_and_slug = True
