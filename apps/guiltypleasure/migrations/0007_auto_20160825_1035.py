# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-25 17:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guiltypleasure', '0006_image_product_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to='apps/guiltypleasure/static/guiltypleasure/images'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=20),
        ),
    ]
