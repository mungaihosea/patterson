# Generated by Django 2.2.7 on 2019-12-28 19:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schoolapp', '0024_timestamp_results'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timestamp',
            name='results',
        ),
    ]