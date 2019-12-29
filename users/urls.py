from django.urls import path

from users.views import ProfileDetails

app_name = 'users'

urlpatterns = [
    path('<int:pk>/profile/details/', ProfileDetails.as_view(), name='details'),
]
