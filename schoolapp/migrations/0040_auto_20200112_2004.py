# Generated by Django 2.2.7 on 2020-01-12 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schoolapp', '0039_gradingsystem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gradingsystem',
            name='grade',
            field=models.CharField(max_length=2),
        ),
    ]
