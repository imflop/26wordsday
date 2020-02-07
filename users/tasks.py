from typing import Optional

from celery import shared_task
from django.db import models

from users.models import User
from utils.email import EmailManager


@shared_task(queue='high', autoretry_for=(Exception, ), max_retries=3)
def send_activation_email(email: str) -> Optional[bool]:
    """
    Задача celery на отправку письма активации
    :param email: str, email пользователя
    :return: Optional[bool]
    """
    if email:
        user = User.objects.filter(models.Q(username=email) | models.Q(email=email)).first()
        if user and not user.is_active:
            EmailManager().send_activation_email(user)

            return True


@shared_task(queue='high', autoretry_for=(Exception, ), max_retries=3)
def send_password_reset_email(email: str) -> Optional[bool]:
    """
    Задача celery на отправку письма с данными о смене пароля
    :param email: str, email пользователя
    :return: Optional[bool]
    """
    if email:
        user = User.objects.filter(models.Q(username=email) | models.Q(email=email)).first()
        if user and user.is_active:
            EmailManager().send_reset_password_email(user)

            return True
