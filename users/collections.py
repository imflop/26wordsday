from django.utils.translation import ugettext_lazy as _


class SupportedLanguages:
    """
    Collection of languages that supported by the system
    """

    ENGLISH = 'english'
    RUSSIAN = 'russian'

    ITEMS = (
        ENGLISH,
        RUSSIAN
    )

    CHOICES = (
        (ENGLISH, _('Английский')),
        (RUSSIAN, _('Русский'))
    )


class SupportedTimezones:
    """
    Collection of supported timezones
    """

    UTC_0300 = 'utc-0300'

    ITEMS = (
        UTC_0300,
    )

    CHOICES = (
        (UTC_0300, _('Europe/Moscow')),
    )


class TimeFormat:
    """
    Collection of time formats
    """

    FORMAT_12_HOUR = '12'
    FORMAT_24_HOUR = '24'

    ITEMS = (
        FORMAT_12_HOUR,
        FORMAT_24_HOUR
    )

    CHOICES = (
        (FORMAT_12_HOUR, _('12-часовой')),
        (FORMAT_24_HOUR, _('24-часовой'))
    )
