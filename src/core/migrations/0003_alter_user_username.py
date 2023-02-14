# Generated by Django 4.1.6 on 2023-02-03 14:17

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(default=uuid.uuid1, max_length=255, unique=True),
        ),
    ]