# Generated by Django 3.1.5 on 2021-02-04 01:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storyapp', '0002_auto_20210203_1738'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='draft_raw',
            field=models.TextField(default='text'),
            preserve_default=False,
        ),
    ]