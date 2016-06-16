# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0028_merge'),
        ('catalogue', '0009_auto_20160616_1038'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={},
        ),
        migrations.RemoveField(
            model_name='category',
            name='depth',
        ),
        migrations.RemoveField(
            model_name='category',
            name='description',
        ),
        migrations.RemoveField(
            model_name='category',
            name='id',
        ),
        migrations.RemoveField(
            model_name='category',
            name='image',
        ),
        migrations.RemoveField(
            model_name='category',
            name='numchild',
        ),
        migrations.RemoveField(
            model_name='category',
            name='path',
        ),
        migrations.RemoveField(
            model_name='category',
            name='slug',
        ),
        migrations.AddField(
            model_name='category',
            name='page_ptr',
            field=models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, default='', serialize=False, to='wagtailcore.Page'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(help_text='Category name', max_length=255, verbose_name='name'),
        ),
    ]
