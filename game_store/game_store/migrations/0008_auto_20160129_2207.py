# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game_store', '0007_payment_ref'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='activation_key',
            field=models.CharField(default=b'', max_length=32),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='is_developer',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
