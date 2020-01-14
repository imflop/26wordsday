# Generated by Django 2.2.4 on 2019-12-27 00:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20190716_1716'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='notification',
        ),
        migrations.RemoveField(
            model_name='user',
            name='phone_number',
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(blank=True, default='', max_length=32, verbose_name='Номер телефона')),
                ('enable_notifications', models.BooleanField(default=False, verbose_name='Уведомления')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Аватар')),
                ('language', models.CharField(choices=[('english', 'Английский'), ('russian', 'Русский')], default='russian', max_length=100, verbose_name='Язык')),
                ('timezone', models.CharField(choices=[('utc-0300', 'Europe/Moscow')], default='utc-0300', max_length=100, verbose_name='Часовой пояс')),
                ('time_format', models.CharField(choices=[('12', '12-часовой'), ('24', '24-часовой')], default='24', max_length=2, verbose_name='Формат времени')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Профиль пользователя',
                'verbose_name_plural': 'Профили пользователей',
            },
        ),
        migrations.CreateModel(
            name='UserToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=False, verbose_name='Активен')),
                ('token', models.CharField(max_length=500, verbose_name='Токен')),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.UserProfile')),
            ],
            options={
                'verbose_name': 'Токен пользователя',
                'verbose_name_plural': 'Токены пользователей',
                'unique_together': {('user_profile', 'token')},
            },
        ),
        migrations.CreateModel(
            name='UserEmail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=False, verbose_name='Активен')),
                ('email', models.EmailField(max_length=50, verbose_name='E-mail')),
                ('verified', models.BooleanField(default=False)),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.UserProfile')),
            ],
            options={
                'verbose_name': 'Email пользователя',
                'verbose_name_plural': 'Email пользователей',
                'unique_together': {('user_profile', 'email')},
            },
        ),
    ]
