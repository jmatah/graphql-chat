# Generated by Django 3.2.3 on 2022-04-12 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_auto_20220412_1919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='read',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
