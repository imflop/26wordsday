from random import choice
from typing import Optional

from celery import shared_task
from django.conf import settings
from django.core.cache import cache

from utils.utils import get_key_from_datetime_now, get_translation
from words.models import Word


@shared_task(queue='high')
def get_twenty_six_words_of_day() -> Optional[bool]:
    """
    Периодическая задача celery на подбор случайных слов
    :return: Optional[bool]
    """
    querysets = []
    for _ in settings.ALPHABET:
        ids = Word.objects.filter(first_letter=_).values_list('pk', flat=True)
        if ids:
            item = Word.objects.filter(pk=choice(ids)).first()
            if item.translation is '' and item.transcription is '':
                result = get_translation(item.text)
                item.translation = result.get('translation')
                item.transcription = result.get('transcription')
                print(f'{item.text}:{item.translation}:{item.transcription}')
                item.save()
            querysets.append(item)
    cache.set(get_key_from_datetime_now(), querysets, timeout=None)
    return True
