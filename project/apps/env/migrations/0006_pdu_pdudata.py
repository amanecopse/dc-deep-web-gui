# Generated by Django 3.2.3 on 2022-08-10 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('env', '0005_delete_pdudata'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pdu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rackNum', models.IntegerField()),
                ('pduNum', models.IntegerField()),
                ('outputCount', models.IntegerField()),
                ('ip', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='PduData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateTime', models.DateTimeField(auto_now_add=True)),
                ('rackNum', models.IntegerField()),
                ('pduNum', models.IntegerField()),
                ('outputNum', models.IntegerField()),
                ('ip', models.CharField(max_length=20)),
                ('current', models.DecimalField(decimal_places=2, max_digits=20)),
                ('power', models.DecimalField(decimal_places=2, max_digits=20)),
                ('energyCounter', models.DecimalField(decimal_places=2, max_digits=20)),
                ('tpf', models.DecimalField(decimal_places=2, max_digits=20)),
                ('phaseShift', models.DecimalField(decimal_places=2, max_digits=20)),
                ('reverseEnergyCounter', models.DecimalField(decimal_places=2, max_digits=20)),
            ],
        ),
    ]
