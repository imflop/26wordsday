from users.models import User

import pytest


@pytest.mark.django_db
def test_user_create():
    User.objects.create_user(
        username='john',
        first_name='',
        last_name='',
        email='john@gmail.com',
        password='johnpassword',
    )
    assert User.objects.count() == 1
