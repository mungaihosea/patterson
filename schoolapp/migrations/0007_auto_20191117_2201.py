# Generated by Django 2.2.7 on 2019-11-17 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schoolapp', '0006_auto_20191117_2135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='english_score',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='mathematics_score',
            field=models.IntegerField(null=True),
        ),
    ]