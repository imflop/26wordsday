import datetime
import json
import re
import unicodedata
from string import ascii_lowercase

import pytz


class Words:
    def __init__(self):
        self.words = self._load_words()
        self.fixture = []
        self.alphabet = list(ascii_lowercase)
        self.alphabet_dict = {k: v for v, k in enumerate(self.alphabet, start=1)}

    def create_fixture(self):
        with open('init_words.json', 'w', encoding='utf-8') as f:
            data = self._create_fixture()
            f.write(json.dumps(data, indent=4))

    def _create_fixture(self) -> list:
        for idx, word in enumerate(self.words, start=1):
            letters_number = self._get_number_of_letters(word)
            time_now_tz = self._get_time()
            word_item = {
                "model": "words.word",
                "pk": int(idx),
                "fields": {
                    "text": str(word),
                    "slug": self._get_slugify(word),
                    "translation": "",
                    "transcription": "",
                    "created_at": time_now_tz,
                    "updated_at": time_now_tz,
                    "number_of_letters": letters_number,
                    "first_letter": word[0]
                }
            }
            self.fixture.append(word_item)
        return self.fixture

    def _load_words(self) -> tuple:
        with open('words_dictionary.json', 'r') as f:
            data_store = json.load(f)
            words = *data_store.keys(),
        return words

    def _get_slugify(self, value: str, allow_unicode=False) -> str:
        value = str(value)
        if allow_unicode:
            value = unicodedata.normalize('NFKC', value)
        else:
            value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
        value = re.sub(r'[^\w\s-]', '', value).strip().lower()
        return re.sub(r'[-\s]+', '-', value)

    def _get_number_of_letters(self, word) -> int:
        return sum(1 for _ in word)

    def _get_time(self) -> str:
        utc_now = pytz.utc.localize(datetime.datetime.utcnow())
        pst_now = utc_now.astimezone(pytz.timezone('Europe/Moscow'))
        return str(pst_now.isoformat())

    def count_words(self, letter: str) -> int:
        count = 0
        words = self._load_words()
        for word in words:
            if word[0] == letter:
                count += 1
        return count


if __name__ == '__main__':
    w = Words()
    w.create_fixture()
