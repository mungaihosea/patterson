# Generated by Django 2.2.7 on 2020-01-11 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schoolapp', '0034_auto_20200110_0553'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='subjects',
            field=models.ManyToManyField(to='schoolapp.Subject'),
        ),
    ]