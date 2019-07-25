from datetime import datetime

import requests
from django.conf import settings


def get_key_from_datetime_now() -> str:
    return f'{datetime.now().strftime("%Y:%m:%d")}'


def get_translation(word: str) -> dict:
    # TODO: привести метод в порядок
    EN_RU = "en-ru"
    response = requests.get(
        f'https://dictionary.yandex.net/api/v1/dicservice.json/lookup?key={settings.YD_KEY}&lang={EN_RU}&text={word}'
    )
    translation = ''
    transcription = ''
    if response.status_code is 200:
        r = response.json()
        if r['def']:
            translation = r['def'][0]['tr'][0]['text']
            if r['def'][0].get('ts'):
                transcription = r['def'][0]['ts']
    return dict(translation=translation, transcription=transcription)

