# Generated by Django 2.2.7 on 2019-12-13 22:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schoolapp', '0020_remove_teacher_selectedsubjectid'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='selectedSubject',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='schoolapp.Subject'),
        ),
    ]
