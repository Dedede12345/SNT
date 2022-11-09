# Generated by Django 4.1.2 on 2022-10-31 10:04

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('body', models.CharField(max_length=255)),
                ('slug', models.SlugField()),
                ('status', models.CharField(choices=[('DF', 'Drafted'), ('PB', 'Published')], default='DF', max_length=2)),
                ('publish', models.TimeField(default=datetime.datetime(2022, 10, 31, 10, 4, 38, 180032, tzinfo=datetime.timezone.utc))),
                ('created', models.TimeField(auto_now_add=True)),
                ('updated', models.TimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notes', to=settings.AUTH_USER_MODEL)),
            ],
            managers=[
                ('draft', django.db.models.manager.Manager()),
            ],
        ),
    ]
