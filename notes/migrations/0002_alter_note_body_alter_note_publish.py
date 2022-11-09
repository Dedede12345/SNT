# Generated by Django 4.1.2 on 2022-11-02 09:02

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='body',
            field=models.TextField(max_length=255),
        ),
        migrations.AlterField(
            model_name='note',
            name='publish',
            field=models.TimeField(default=django.utils.timezone.now),
        ),
    ]
