# Generated by Django 2.2.10 on 2021-06-10 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='tweet_handle',
            field=models.CharField(default='none', max_length=100),
            preserve_default=False,
        ),
    ]