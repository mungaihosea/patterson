# Generated by Django 2.2.7 on 2019-12-31 18:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schoolapp', '0026_timestamp_results'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='class_teacher_grade',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='schoolapp.Grade'),
        ),
        migrations.AddField(
            model_name='teacher',
            name='class_teacher_stream',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='schoolapp.Stream'),
        ),
    ]