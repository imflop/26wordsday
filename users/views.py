from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView
from django.shortcuts import render
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.generic import TemplateView, FormView, DetailView
from django.views.generic.edit import BaseFormView

from users.forms import UserAuthenticationForm, UserPasswordResetForm, UserRegistrationForm, \
    UserPasswordResetConfirmForm, UserAccountActivationRepeat
from users.models import User, UserProfile
from users.tasks import send_activation_email, send_password_reset_email


class UserLoginView(LoginView):
    """
    Представление для входа в систему
    """
    form_class = UserAuthenticationForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        if 'remember_me' not in form.cleaned_data:
            self.request.session.set_expiry(settings.SET_EXPIRY)
        return super().form_valid(form)


class AccountActivationDoneView(TemplateView):
    """
    Представление для окна успешной активации аккаунта
    """
    template_name = 'registration/account_activation_done.html'


class AccountActivationConfirmView(View):
    """
    Представление для активации аккаунта пользователя
    """
    def get(self, request, uidb64=None, token=None):
        uid = urlsafe_base64_decode(uidb64)
        user = User.objects.filter(pk=uid).first()

        if user is not None and default_token_generator.check_token(user, token):
            user.email_confirmed = True
            user.is_active = True
            user.save()

            return render(request, 'registration/account_activation_confirm.html')
        else:
            return render(request, 'registration/account_activation_failed.html')


class UserPasswordResetView(PasswordResetView):
    """
    Представление для сброса пароля пользователем (ввод Email)
    """
    form_class = UserPasswordResetForm

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        send_password_reset_email.delay(email=email)

        return super(BaseFormView, self).form_valid(form)


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    """
    Представление для сброса пароля пользователем (ввод нового пароля)
    """
    form_class = UserPasswordResetConfirmForm


class UserRegistrationView(FormView):
    """
    Представление для регистрации пользователя
    """
    template_name = 'registration/registration.html'
    form_class = UserRegistrationForm
    success_url = '/activate/done/'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.email = user.username
        user.is_active = False
        user.set_password(form.cleaned_data.get('password'))
        user.save()
        send_activation_email.delay(email=user.email)

        return super().form_valid(form)


class SendActivationEmail(FormView):
    """
    Представление для отправки Email активации аккаунта
    """
    template_name = 'registration/account_activation_repeat.html'
    form_class = UserAccountActivationRepeat
    success_url = '/activate/done/'

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        send_activation_email.delay(email=email)

        return super().form_valid(form)


class ProfileDetails(DetailView):
    """
    Profile details subpage
    """

    model = UserProfile
    template_name = 'profile/details.html'
