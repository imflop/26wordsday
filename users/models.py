from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from users.collections import SupportedLanguages, SupportedTimezones, TimeFormat


class User(AbstractUser):
    """
    Main user model
    """

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')

    def __str__(self):
        return self.email


class UserProfile(models.Model):
    """
    User profile model
    """

    user = models.OneToOneField('User', related_name='profile', on_delete=models.CASCADE)
    phone_number = models.CharField(verbose_name=_('Номер телефона'), max_length=32, default='', blank=True)
    enable_notifications = models.BooleanField(verbose_name=_('Уведомления'), default=False)
    avatar = models.ImageField(verbose_name=_('Аватар'), blank=True, null=True)
    language = models.CharField(verbose_name=_('Язык'), max_length=100, choices=SupportedLanguages.CHOICES,
                                default=SupportedLanguages.RUSSIAN)
    timezone = models.CharField(verbose_name=_('Часовой пояс'), max_length=100, choices=SupportedTimezones.CHOICES,
                                default=SupportedTimezones.UTC_0300)
    time_format = models.CharField(verbose_name=_('Формат времени'), max_length=2, choices=TimeFormat.CHOICES,
                                   default=TimeFormat.FORMAT_24_HOUR)

    class Meta:
        verbose_name = _('Профиль пользователя')
        verbose_name_plural = _('Профили пользователей')

    def __str__(self):
        return str(self.user)


class UserProfileRelatedCollector(models.Model):
    """
    Abstract class for profile simple relations
    """

    user_profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    is_active = models.BooleanField(verbose_name=_('Активен'), default=False)

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.user_profile.user)


class UserEmail(UserProfileRelatedCollector):
    """
    User emails collector-model
    """

    email = models.EmailField(verbose_name=_('E-mail'), max_length=50)
    verified = models.BooleanField(default=False)

    class Meta:
        unique_together = (('user_profile', 'email'),)
        verbose_name = _('Email пользователя')
        verbose_name_plural = _('Email пользователей')


class UserToken(UserProfileRelatedCollector):
    """
    User tokens collector-model
    """

    token = models.CharField(verbose_name=_('Токен'), max_length=500)

    class Meta:
        unique_together = (('user_profile', 'token'),)
        verbose_name = _('Токен пользователя')
        verbose_name_plural = _('Токены пользователей')


@receiver(post_save, sender=User)
def create_user_profile(sender, instance: User, created: bool, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
