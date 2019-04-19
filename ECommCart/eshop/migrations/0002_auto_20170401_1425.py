# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('eshop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('terms_condition', models.CharField(max_length=1, choices=[('T', 'True'), ('F', 'False')])),
                ('activation_key', models.CharField(null=True, max_length=40, blank=True)),
                ('key_expires', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_alive', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, related_name='user_profile')),
            ],
        ),
        migrations.RemoveField(
            model_name='customerprofile',
            name='user',
        ),
        migrations.DeleteModel(
            name='CustomerProfile',
        ),
    ]
