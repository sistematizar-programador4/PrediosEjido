# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0006_auto_20160122_1313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='propieta',
            name='email',
            field=models.CharField(default=b'-', max_length=50, null=True, blank=True),
        ),
    ]
