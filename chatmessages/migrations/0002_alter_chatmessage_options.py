# Generated by Django 3.2 on 2022-08-22 02:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chatmessages', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chatmessage',
            options={'ordering': ['-id']},
        ),
    ]