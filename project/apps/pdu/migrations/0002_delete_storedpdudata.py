# Generated by Django 3.2.3 on 2022-08-10 13:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pdu', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='StoredPduData',
        ),
    ]