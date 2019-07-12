from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    notification = models.BooleanField(verbose_name=_('Уведомления'), default=False)
    phone_number = models.CharField(verbose_name=_('Номер телефона'), max_length=32, default=0)

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')

    def __str__(self):
        return self.email
