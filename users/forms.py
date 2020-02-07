from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from flex_forms.components import FlexButton, BaseButton, StaticFlexField, FlexDataArray
from flex_forms.forms import FlexForm, FlexModelForm, FlexFormErrorsMixin

from users.models import User
from utils.components import BaseLink, DescriptionLink


class SignInFlexForm(FlexFormErrorsMixin, FlexForm, AuthenticationForm):
    """
    Форма для входа пользователя в систему.
    """

    css_classes = ['flex-form', 'sign-in-form']
    html_params = {'novalidate': '', 'method': 'POST'}
    grid = {
        '_1': ['username'],
        '_2': ['password'],
        '_3': ['remember_me', 'lost_password'],
        '_4': ['submit'],
        '_5': ['sign_up'],
        '_6': ['form_errors']
    }
    remember_me = forms.BooleanField(label=_('Remember me'), required=False, widget=forms.CheckboxInput())
    submit = FlexButton(BaseButton(_('Sign In'), css_classes=['btn-normal-blue'], html_params={'type': 'submit'}))
    lost_password = FlexButton(BaseLink(_('Lost password'), html_params={'href': reverse_lazy('password_reset')}))
    sign_up = FlexButton(
        DescriptionLink(_("Don't have an account?"), _('Sign Up'), html_params={'href': reverse_lazy('sign_up')})
    )
    form_errors = FlexDataArray(label=_('Error'), help_text=_('Please, fix to continue'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = _('Username or Email')
        self.fields['username'].widget.attrs['autocomplete'] = 'off'
        self.fields['password'].widget.attrs['placeholder'] = _('Password')


class SignInLandingFlexForm(SignInFlexForm):
    """
    Форма для входа пользователя в систему на странице landing.
    """

    html_params = {'novalidate': '', 'method': 'POST', 'id': 'landing-auth-form'}
    submit = FlexButton(
        BaseButton(
            _('Sign In'), css_classes=['btn-normal-blue'],
            html_params={
                'type': 'button',
                'data-ajax-post-type': 'landing_auth',
                'data-ajax-form': '#landing-auth-form',
                'data-ajax-container': '#auth .js-window_body_content'
            }
        )
    )


class SignUpFlexForm(FlexFormErrorsMixin, FlexModelForm):
    """
    Форма для регистрации пользователя.
    """
    css_classes = ['flex-form', 'sign-up-form']
    html_params = {'novalidate': '', 'method': 'POST'}
    grid = {
        '_1': ['username'],
        '_2': ['email'],
        '_3': ['password'],
        '_4': ['password_repeat'],
        '_5': ['submit'],
        '_6': ['sign_in'],
        '_7': ['activation_repeat']
    }
    password_repeat = forms.CharField(widget=forms.PasswordInput())
    password = forms.CharField(widget=forms.PasswordInput())
    submit = FlexButton(BaseButton(_('Sign Up'), css_classes=['btn-normal-blue'], html_params={'type': 'submit'}))
    sign_in = FlexButton(DescriptionLink(_("Already have an account?"), _('Sign In'),
                                         html_params={'href': reverse_lazy('sign_in')}))
    activation_repeat = FlexButton(DescriptionLink(_("Did not receive an activation letter?"), _('Repeat activation'),
                                                   html_params={'href': reverse_lazy('activation_repeat')}))
    form_errors = FlexDataArray(label=_('Error'), help_text=_('Please, fix to continue'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = _('Username')
        self.fields['username'].widget.attrs['autofocus'] = True
        self.fields['username'].widget.attrs['autocomplete'] = 'off'
        self.fields['username'].help_text = None
        self.fields['email'].widget.attrs['placeholder'] = _('Email')
        self.fields['password'].widget.attrs['placeholder'] = _('Password')
        self.fields['password_repeat'].widget.attrs['placeholder'] = _('Repeat password')

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

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


class UserPasswordResetFlexForm(FlexForm):
    """
    Форма для ввода Email и начала операций по восстановлению пароля пользователя.
    """

    css_classes = ['flex-form', 'password-reset-form']
    html_params = {'novalidate': '', 'method': 'POST'}
    grid = {
        '_1': ['description'],
        '_2': ['email'],
        '_3': ['submit']
    }
    email = forms.EmailField(max_length=254)
    description = StaticFlexField(_('Please enter the email address associated with your 26wordsday.com account.'))
    submit = FlexButton(BaseButton(_('Continue'), css_classes=['btn-normal-blue'], html_params={'type': 'submit'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = _('Email')
        self.fields['email'].widget.attrs['autocomplete'] = 'off'


class UserAccountActivationRepeatFlexForm(UserPasswordResetFlexForm):
    """
    Форма повторной активации аккаунта пользователя.
    """

    pass


class UserPasswordResetConfirmFlexForm(FlexForm, SetPasswordForm):
    """
    Форма для ввода нового пароля пользователем.
    """

    css_classes = ['flex-form', 'password-confirm-form']
    html_params = {'novalidate': '', 'method': 'POST'}
    grid = {
        '_1': ['description'],
        '_2': ['new_password1'],
        '_3': ['new_password2'],
        '_4': ['submit']
    }
    email = forms.EmailField(max_length=254)
    description = StaticFlexField(_('Please enter a new password for your 26wordsday.com account.'))
    submit = FlexButton(BaseButton(_('Continue'), css_classes=['btn-normal-blue'], html_params={'type': 'submit'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs['placeholder'] = _('New password')
        self.fields['new_password2'].widget.attrs['placeholder'] = _('Repeat Password')
