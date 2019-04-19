# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('date_of_order', models.DateTimeField(default=django.utils.timezone.now)),
                ('sum_of_prod_cost', models.PositiveIntegerField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='CustomerProfile',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('terms_condition', models.CharField(max_length=1, choices=[('T', 'True'), ('F', 'False')])),
                ('activation_key', models.CharField(max_length=40, null=True, blank=True)),
                ('key_expires', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_alive', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, related_name='user_profile')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=50)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('prod_cat', models.CharField(max_length=1, choices=[('C', 'Clothes'), ('F', 'Food'), ('O', 'Office')])),
                ('cost_of_each', models.PositiveIntegerField(null=True, blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='user_id')),
            ],
        ),
        migrations.CreateModel(
            name='ProductOrderStatus',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('quantity_of_each_product', models.PositiveIntegerField(null=True, blank=True)),
                ('order', models.ForeignKey(to='eshop.Cart', related_name='Cart_details')),
                ('prod', models.ForeignKey(to='eshop.Product', related_name='prod_det')),
            ],
        ),
        migrations.CreateModel(
            name='UserOrderStatus',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('status', models.CharField(default='P', max_length=1, choices=[('S', 'Start'), ('M', 'Payment'), ('E', 'Shipped'), ('D', 'Delivered'), ('P', 'Pending')])),
                ('order', models.ForeignKey(to='eshop.Cart', related_name='Cart_det')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='user_of_game')),
            ],
        ),
        migrations.AddField(
            model_name='cart',
            name='prod_details',
            field=models.ForeignKey(to='eshop.Product', related_name='product_in_order'),
        ),
        migrations.AddField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='user_of_order'),
        ),
    ]
