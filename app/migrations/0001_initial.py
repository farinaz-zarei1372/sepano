# Generated by Django 4.2.1 on 2023-06-27 06:26

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_shop_owner', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('username', models.CharField(max_length=30)),
                ('gender', models.CharField(choices=[('male', 'male'), ('female', 'female')], max_length=10)),
                ('birthdate', models.DateField(default=datetime.datetime.now)),
                ('phonenumber', models.CharField(max_length=11, unique=True, validators=[django.core.validators.RegexValidator('09(1[0-9]|3[1-9]|2[1-9])-?[0-9]{3}-?[0-9]{4}', 'Only digit  and 11 characters with 0 at first of that.', code='invalid_phonenumber')])),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
