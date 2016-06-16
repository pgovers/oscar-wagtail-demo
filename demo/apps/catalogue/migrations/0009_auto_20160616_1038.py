# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0008_auto_20160304_1652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productattributevalue',
            name='value_file',
            field=models.FileField(max_length=255, null=True, upload_to=b'/Users/hj.vanhasselaar/Projects/wagtail/oscar-wagtail-demo/wagtaildemo/settings/../../demo/static/demo/images', blank=True),
        ),
        migrations.AlterField(
            model_name='productattributevalue',
            name='value_image',
            field=models.ImageField(max_length=255, null=True, upload_to=b'/Users/hj.vanhasselaar/Projects/wagtail/oscar-wagtail-demo/wagtaildemo/settings/../../demo/static/demo/images', blank=True),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='original',
            field=models.ImageField(upload_to=b'/Users/hj.vanhasselaar/Projects/wagtail/oscar-wagtail-demo/wagtaildemo/settings/../../demo/static/demo/images', max_length=255, verbose_name='Original'),
        ),
    ]
