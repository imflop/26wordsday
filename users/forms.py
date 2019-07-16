from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.utils.translation import ugettext_lazy as _

from users.models import User
from utils.forms import StyledForm


class UserAuthenticationForm(StyledForm, AuthenticationForm):
    """
    Форма для входа пользователя в систему (Расширение стандартной формы 'AuthenticationForm')
    """
    remember_me = forms.BooleanField(label=_('Запомнить меня'), required=False, widget=forms.CheckboxInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] += ' form-control floating-label-input'
        self.fields['username'].widget.attrs['placeholder'] = 'Email'
        self.fields['username'].widget.attrs['id'] = 'id_username'
        self.fields['username'].widget.attrs['type'] = 'email'

        self.fields['password'].widget.attrs['class'] += ' form-control floating-label-input'
        self.fields['password'].widget.attrs['placeholder'] = _('Пароль')
        self.fields['password'].widget.attrs['id'] = 'id_password'

        self.fields['remember_me'].widget.attrs['class'] += ' remember-me-checkbox'


class UserPasswordResetForm(StyledForm):
    """
    Форма для сброса пароля пользователем (Расширение стандартной формы 'PasswordResetForm')
    """
    email = forms.EmailField(label=_('Email'), max_length=254)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['class'] += ' form-control floating-label-input'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['email'].widget.attrs['id'] = 'id_email'


class UserAccountActivationRepeat(UserPasswordResetForm):
    """
    Форма повторной активации аккаунта пользователя
    """
    pass


class UserPasswordResetConfirmForm(StyledForm, SetPasswordForm):
    """
    Форма для сброса пароля пользователя
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs['class'] += ' form-control floating-label-input'
        self.fields['new_password1'].widget.attrs['placeholder'] = _('Новый пароль')
        self.fields['new_password1'].widget.attrs['id'] = 'new_password1'

        self.fields['new_password2'].widget.attrs['class'] += ' form-control floating-label-input'
        self.fields['new_password2'].widget.attrs['placeholder'] = _('Повторите пароль')
        self.fields['new_password2'].widget.attrs['id'] = 'new_password2'


class UserRegistrationForm(StyledForm, forms.ModelForm):
    """
    Форма для регистрации пользователя
    """
    password_repeat = forms.CharField(
        label=_('Повторите пароль'),
        widget=forms.PasswordInput(attrs={
            'id': 'id_password_repeat',
            'class': 'form-control floating-label-input',
        }))

    class Meta:
        model = User
        fields = ('password', 'username', )
        widgets = {
            'username': forms.EmailInput(attrs={
                'id': 'id_username',
                'class': 'form-control floating-label-input',
                'placeholder': 'Email'
            }),
            'password': forms.PasswordInput(attrs={
                'id': 'id_password',
                'class': 'form-control floating-label-input',
                'placeholder': _('Пароль')
            }),
            'phone_number': forms.TextInput(attrs={
                'id': 'id_phone_number',
                'class': 'form-control floating-label-input',
                'type': 'tel',
                'placeholder': _('Номер телефона')
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password_repeat'].widget.attrs['class'] += ' form-control floating-label-input'
        self.fields['password_repeat'].widget.attrs['placeholder'] = _('Повторите пароль')
        self.fields['password_repeat'].widget.attrs['id'] = 'id_password_repeat'

    def clean(self):
        """
        Проверка повторно введенного пароля
        """
        super().clean()

        password = self.cleaned_data.get('password')
        password_repeat = self.cleaned_data.get('password_repeat')
        if password and password_repeat:
            if password != password_repeat:
                self.add_error(None, _('Пароли не совпадают'))

        # Валидация пароля
        password = self.cleaned_data.get('password')
        password_validation.validate_password(password)

        return self.cleaned_data
