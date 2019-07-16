from typing import Optional

from celery import shared_task


@shared_task(queue='high')
def get_twenty_six_words_of_day() -> Optional[bool]:
    """
    Периодическая задача celery на подбор случайных слов
    :return: Optional[bool]
    """
    return True
