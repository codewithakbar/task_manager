# Generated by Django 4.2.1 on 2023-10-01 20:14

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("trello", "0004_board_user"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="board",
            name="user",
        ),
        migrations.AddField(
            model_name="board",
            name="user",
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]