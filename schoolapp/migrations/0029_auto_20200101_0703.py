# Generated by Django 2.2.7 on 2020-01-01 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schoolapp', '0028_auto_20200101_0703'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='age',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
