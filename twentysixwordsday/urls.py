"""twentysixwordsday URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from django.conf.urls.static import static

from users.views import AccountActivationDoneView, AccountActivationConfirmView, \
    SendActivationEmail, SignInLandingFormView, SignInFormView, \
    SignUpFormView, PasswordResetFormView, PasswordResetConfirmFormView, PasswordResetDoneView, \
    PasswordResetCompleteView, PasswordResetUnsuccessfulView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('words/', include('words.urls')),
    path('users/', include('users.urls')),

    # Auth
    path('', SignInLandingFormView.as_view(), name='landing'),
    path('sign-in/', SignInFormView.as_view(), name='sign_in'),
    path('sign-up/', SignUpFormView.as_view(), name='sign_up'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # Account Activation
    path('activate/done/', AccountActivationDoneView.as_view(), name='activation_done'),
    path('activate/confirm/<uidb64>/<token>/', AccountActivationConfirmView.as_view(), name='activation_confirm'),
    path('activate/repeat/', SendActivationEmail.as_view(), name='activation_repeat'),

    # Password Reset
    path('password-reset/', PasswordResetFormView.as_view(), name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/unsuccessful/', PasswordResetUnsuccessfulView.as_view(), name='password_reset_unsuccessful'),
    path('password-reset/confirm/<uidb64>/<token>/', PasswordResetConfirmFormView.as_view(), name="password_reset_confirm"),
    path('password-reset/complete/', PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += (
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )

if not settings.DEBUG:
    handler400 = 'twentysixwordsday.views.error_400_view'
    handler403 = 'twentysixwordsday.views.error_403_view'
    handler404 = 'twentysixwordsday.views.error_404_view'
    handler500 = 'twentysixwordsday.views.error_500_view'
