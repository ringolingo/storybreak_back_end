# Generated by Django 3.1.5 on 2021-02-14 05:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('storyapp', '0008_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='stories', to='storyapp.user'),
            preserve_default=False,
        ),
    ]
