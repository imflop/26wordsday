from django.contrib import admin
from .models import Word, WordStat


@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ('text', 'translation', 'transcription')
    search_fields = ('text', 'translation')
    ordering = ('text',)


@admin.register(WordStat)
class WordStatAdmin(admin.ModelAdmin):
    list_display = ('is_used', 'date_used')

