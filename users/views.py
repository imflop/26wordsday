from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import ugettext_lazy as _
from django.views import View
from django.views.generic import TemplateView, FormView, DetailView
from django.views.generic.edit import BaseFormView

from users.forms import SignInFlexForm, SignInLandingFlexForm, SignUpFlexForm, UserPasswordResetFlexForm, \
    UserPasswordResetConfirmFlexForm, UserAccountActivationRepeatFlexForm
from users.models import User, UserProfile
from users.tasks import send_activation_email, send_password_reset_email
from utils.components import Img, Link
from utils.mixins import TitleViewMixin, MessageViewMixin, CustomFormViewMixin


class SignInBaseView(TitleViewMixin, LoginView):
    """
    Базовое представление для входа пользователя в систему.
    """

    redirect_authenticated_user = True
    title = _('Sign In')

    def form_valid(self, form):
        if 'remember_me' not in form.cleaned_data:
            self.request.session.set_expiry(settings.SET_EXPIRY)
        return super().form_valid(form)


class SignInFormView(SignInBaseView):
    """
    Представление для поддержки входа пользователя в систему.
    """

    form_class = SignInFlexForm
    template_name = 'registration/base_auth.html'


class SignInLandingFormView(CustomFormViewMixin, SignInBaseView):
    """
    Представление для поддержки быстрого входа пользователя в систему со стороны landing page (модальное окно).
    """

    form_class = SignInLandingFlexForm
    template_name = 'landing.html'


class SignUpFormView(TitleViewMixin, FormView):
    """
    Представление для регистрации пользователя в системе.
    """

    model = User
    form_class = SignUpFlexForm
    template_name = 'registration/base_auth.html'
    success_url = '/activate/done/'
    title = _('Sign Up')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.set_password(form.cleaned_data.get('password'))
        user.save()
        send_activation_email.delay(email=user.email)

        return super().form_valid(form)


class PasswordResetFormView(PasswordResetView):
    """
    Представление для сброса пароля пользователем (ввод Email).
    """

    form_class = UserPasswordResetFlexForm
    template_name = 'registration/base_auth.html'
    # title установлен в PasswordResetView

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        send_password_reset_email.delay(email=email)

        return super(BaseFormView, self).form_valid(form)


class PasswordResetConfirmFormView(PasswordResetConfirmView):
    """
    Представление установки нового пароля пользователем.
    """

    form_class = UserPasswordResetConfirmFlexForm
    template_name = 'registration/base_auth.html'
    # title установлен в PasswordResetConfirmView

    def dispatch(self, *args, **kwargs):
        response = super().dispatch(*args, **kwargs)
        if not self.validlink:
            response = redirect('password_reset_unsuccessful')
        return response


class SendActivationEmail(TitleViewMixin, FormView):
    """
    Представление для отправки Email активации аккаунта
    """

    template_name = 'registration/base_auth.html'
    form_class = UserAccountActivationRepeatFlexForm
    success_url = '/activate/done/'
    title = _('Repeat activation')

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        send_activation_email.delay(email=email)

        return super().form_valid(form)


class AccountActivationDoneView(MessageViewMixin, TemplateView):
    """
    Представление для окна сообщения об отправке сообщения на почту регистрирующегося пользователя.
    """

    template_name = 'system.html'

    message_icon = Img(html_params={'src': '/assets/img/logo_big_anim_4.png', 'width': '120', 'height': '120'})
    message_subject = _('We sent you a message to confirm your account. You should receive it soon.')
    message_text = _('If you have not received an email, please make sure that you have entered the correct address '
                     'or check the spam folder.')


class AccountActivationConfirmView(View):
    """
    Представление для активации аккаунта пользователя.
    """

    template_name = 'system.html'

    def get(self, request, uidb64=None, token=None):
        uid = urlsafe_base64_decode(uidb64)

        try:
            user = User.objects.filter(pk=uid).first()
        except Exception:
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()

            context = dict(
                message_subject=_('Your account has been successfully verified!'),
                message_text=_('To log in, go to the login page.'),
                message_icon=Img(html_params={'src': '/assets/img/logo_big_anim_4.png',
                                              'width': '120', 'height': '120'})
            )

            response = render(request, self.template_name, context)
        else:
            context = dict(
                message_subject=_('User not found or activation timed out.'),
                message_text=_('Please use the account reactivation form or try registering again.'),
                message_icon=Img(html_params={'src': '/assets/img/logo_big_anim_3.png',
                                              'width': '200', 'height': '200'})
            )
            response = render(request, self.template_name, context)

        return response


class PasswordResetDoneView(MessageViewMixin, TemplateView):
    """
    Представление для окна с сообщением от отправке Email c данными по сбросу пароля.
    """

    template_name = 'system.html'

    message_icon = Img(html_params={'src': '/assets/img/logo_big_anim_4.png', 'width': '120', 'height': '120'})
    message_subject = _('We have sent you password recovery instructions. You should get it soon.')
    message_text = _('If you have not received an email, please make sure that you have entered the correct address '
                     'or check the spam folder.')


class PasswordResetUnsuccessfulView(MessageViewMixin, TemplateView):
    """
    Представление для окна с сообщением о невозможности сброса пароля.
    """

    template_name = 'system.html'

    message_icon = Img(html_params={'src': '/assets/img/logo_big_anim_3.png', 'width': '200', 'height': '200'})
    message_subject = _('Password reset token expired.')
    message_text = _('Please try resetting your password again.')
    message_link = Link(_('Reset password'), html_params={'href': reverse_lazy('password_reset')})


class PasswordResetCompleteView(MessageViewMixin, TemplateView):
    """
    Представление для окна с сообщением об успешной смене пароля.
    """

    template_name = 'system.html'

    message_icon = Img(html_params={'src': '/assets/img/logo_big_anim_4.png', 'width': '120', 'height': '120'})
    message_subject = _('You have successfully changed your password!')
    message_text = _('Now you can log in with the new password using the link below.')
    message_link = Link(_('Sign In'), html_params={'href': reverse_lazy('sign_in')})


class ProfileDetails(DetailView):
    """
    Profile details subpage
    """

    model = UserProfile
    template_name = 'profile/details.html'
