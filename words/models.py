from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class WordStat(models.Model):
    is_used = models.BooleanField(verbose_name=_('Использовалось'), default=False)
    date_used = models.DateTimeField(verbose_name=_('Дата использвания'), default=timezone.now)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Пользователь'), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Статистика')
        verbose_name_plural = _('Статистика')

    def __str__(self):
        return f"Used: {self.date_used.strftime('%d.%m.%Y %H:%M:%S')}"


class Word(models.Model):
    text = models.CharField(verbose_name=_('Текст'), max_length=128, unique=True)
    slug = models.CharField(verbose_name=_('Slug'), max_length=128, default='')
    translation = models.CharField(verbose_name=_('Перевод'), max_length=128, blank=True, null=True)
    transcription = models.CharField(verbose_name=_('Транскрипция'), max_length=128, blank=True, null=True)
    created_at = models.DateTimeField(verbose_name=_('Дата добавления'), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('Дата обнолвения'), auto_now=True)
    first_letter = models.CharField(verbose_name=_('Первая буква слова'), max_length=1)
    number_of_letters = models.PositiveIntegerField(verbose_name=_('Количество букв'), default=0)

    class Meta:
        verbose_name = _('Слово')
        verbose_name_plural = _('Слова')

    def __str__(self):
        return self.text
