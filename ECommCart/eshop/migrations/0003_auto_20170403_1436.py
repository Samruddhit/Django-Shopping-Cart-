# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eshop', '0002_auto_20170401_1425'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userorderstatus',
            name='order',
        ),
        migrations.RemoveField(
            model_name='userorderstatus',
            name='user',
        ),
        migrations.AddField(
            model_name='productorderstatus',
            name='status',
            field=models.CharField(default='S', max_length=1, choices=[('S', 'Start'), ('M', 'Payment'), ('E', 'Shipped'), ('D', 'Delivered'), ('P', 'Pending')]),
        ),
        migrations.DeleteModel(
            name='UserOrderStatus',
        ),
    ]
