# Generated by Django 2.2.7 on 2019-12-12 20:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schoolapp', '0017_teacher_selecteddatabase'),
    ]

    operations = [
        migrations.RenameField(
            model_name='report',
            old_name='english_score',
            new_name='english',
        ),
        migrations.RenameField(
            model_name='report',
            old_name='mathematics_score',
            new_name='mathematics',
        ),
    ]