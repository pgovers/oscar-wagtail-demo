# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.wagtailcore.fields
import wagtail.wagtailcore.blocks
import wagtail.wagtailimages.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0011_auto_20160616_1335'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='body',
            field=wagtail.wagtailcore.fields.StreamField([(b'heading', wagtail.wagtailcore.blocks.CharBlock(classname=b'full title')), (b'paragraph', wagtail.wagtailcore.blocks.RichTextBlock()), (b'image', wagtail.wagtailimages.blocks.ImageChooserBlock())]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Name', db_index=True),
        ),
    ]
