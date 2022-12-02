# Generated by Django 4.1.2 on 2022-11-30 15:50

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notes', '0006_alter_note_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='users_liked',
            field=models.ManyToManyField(blank=True, related_name='notes_liked', to=settings.AUTH_USER_MODEL),
        ),
    ]
