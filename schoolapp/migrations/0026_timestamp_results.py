# Generated by Django 2.2.7 on 2019-12-28 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schoolapp', '0025_remove_timestamp_results'),
    ]

    operations = [
        migrations.AddField(
            model_name='timestamp',
            name='results',
            field=models.TextField(null=True),
        ),
    ]