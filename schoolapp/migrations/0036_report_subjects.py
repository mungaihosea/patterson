# Generated by Django 2.2.7 on 2020-01-11 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schoolapp', '0035_auto_20200111_1700'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='subjects',
            field=models.ManyToManyField(to='schoolapp.Subject'),
        ),
    ]
