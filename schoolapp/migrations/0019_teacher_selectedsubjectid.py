# Generated by Django 2.2.7 on 2019-12-13 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schoolapp', '0018_auto_20191212_2027'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='selectedSubjectId',
            field=models.IntegerField(null=True),
        ),
    ]
