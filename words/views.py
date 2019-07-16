from itertools import chain
from random import choice

from django.conf import settings
from django.views.generic import ListView

from .models import Word


class WordListView(ListView):
    model = Word
    template_name = 'words_list.html'
    context_object_name = 'words_list'
    querysets_list = []

    def get_queryset(self):
        qs = super().get_queryset()
        for _ in settings.ALPHABET:
            ids = qs.filter(first_letter=_).values_list('pk', flat=True)
            if ids:
                item = qs.filter(pk=choice(ids))
                self.querysets_list.append(item)
        return list(chain(*self.querysets_list))
