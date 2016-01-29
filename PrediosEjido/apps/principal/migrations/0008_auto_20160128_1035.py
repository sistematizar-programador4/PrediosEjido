# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0007_auto_20160128_1031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='propieta',
            name='email',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
    ]
