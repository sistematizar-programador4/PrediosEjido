# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0005_auto_20151222_1951'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pago',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('c_recaja', models.IntegerField()),
                ('f_recaja', models.DateField()),
                ('v_recaja', models.DecimalField(max_digits=11, decimal_places=2)),
            ],
        ),
        migrations.RemoveField(
            model_name='predio',
            name='c_recaja',
        ),
        migrations.RemoveField(
            model_name='predio',
            name='f_recaja',
        ),
        migrations.RemoveField(
            model_name='predio',
            name='id_propieta_fin',
        ),
        migrations.RemoveField(
            model_name='predio',
            name='v_recaja',
        ),
        migrations.AddField(
            model_name='predio',
            name='propieta_predio',
            field=models.ManyToManyField(to='principal.Propieta', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='propieta',
            name='direction',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='propieta',
            name='email',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='propieta',
            name='tel',
            field=models.IntegerField(max_length=10, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='predio',
            name='propieta',
            field=models.CharField(max_length=80),
        ),
        migrations.AlterField(
            model_name='propieta',
            name='name',
            field=models.CharField(max_length=80),
        ),
        migrations.AddField(
            model_name='pago',
            name='predio',
            field=models.ForeignKey(to='principal.Predio'),
        ),
    ]
