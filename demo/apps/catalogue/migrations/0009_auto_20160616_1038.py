# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0008_auto_20160304_1652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productattributevalue',
            name='value_file',
            field=models.FileField(max_length=255, null=True, upload_to=settings.OSCAR_IMAGE_FOLDER, blank=True),
        ),
        migrations.AlterField(
            model_name='productattributevalue',
            name='value_image',
            field=models.ImageField(max_length=255, null=True, upload_to=settings.OSCAR_IMAGE_FOLDER, blank=True),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='original',
            field=models.ImageField(upload_to=settings.OSCAR_IMAGE_FOLDER, max_length=255, verbose_name='Original'),
        ),
    ]
