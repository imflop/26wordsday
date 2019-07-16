from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.template.loader import get_template
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from users.models import User


class EmailManager:
    """
    Класс-менеджер отправки писем электронной почты
    """
    def email_user(self, user: User, subject: str, message: HttpResponse, from_email: str = None, **kwargs) -> None:
        """
        Метод для отправки email
        :param user: User, целевой пользователь
        :param subject: str, тема сообщения
        :param message: HttpResponse, ответ с шаблоном в виде сообщения
        :param from_email: str, e-mail отправителя
        :param kwargs: dict, доп. аргументы
        :return: None
        """
        message = EmailMessage(subject=subject, body=message, from_email=from_email, to=[user.email])
        if kwargs['content_subtype']:
            message.content_subtype = kwargs['content_subtype']
        message.send()

    def send_activation_email(self, user: User, use_https: bool = settings.USE_HTTPS) -> None:
        """
        Метод для отправки сообщения с данными для активации аккаунта
        :param user: User, целевой пользователь
        :param use_https:bool, протокол HTTPS
        :return: None
        """
        template = get_template('registration/account_activation_email.html')
        ctx = {
            'protocol': 'https' if use_https else 'http',
            'domain': settings.DOMAIN,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
            'user': user
        }
        content = template.render(ctx)

        self.email_user(user=user, subject='Подтверждение аккаунта', message=content, content_subtype='html')

    def send_reset_password_email(self, user: User, use_https: bool = settings.USE_HTTPS) -> None:
        """
        Метод для отправки сообщения с информацией для смены пароля
        :param user: User, целевой пользователь
        :param use_https: bool, протокол HTTPS
        :return: None
        """
        template = get_template('registration/password_reset_email.html')
        ctx = {
            'protocol': 'https' if use_https else 'http',
            'domain': settings.DOMAIN,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
            'user': user
        }
        content = template.render(ctx)

        self.email_user(user=user, subject='Смена пароля', message=content, content_subtype='html')
