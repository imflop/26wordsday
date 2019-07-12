from django.views.generic import ListView
from .models import Word


class WordListView(ListView):
    model = Word
    template_name = 'words_list.html'
    context_object_name = 'words_list'
