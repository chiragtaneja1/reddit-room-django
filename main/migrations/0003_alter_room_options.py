# Generated by Django 4.0 on 2021-12-26 15:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='room',
            options={'ordering': ['-created', '-updated']},
        ),
    ]
