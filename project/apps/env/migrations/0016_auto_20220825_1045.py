# Generated by Django 3.2.3 on 2022-08-25 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('env', '0015_auto_20220816_1450'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sensordata',
            old_name='value',
            new_name='humidity',
        ),
        migrations.RemoveField(
            model_name='sensordata',
            name='dataType',
        ),
        migrations.RemoveField(
            model_name='sensordata',
            name='dataUnit',
        ),
        migrations.AddField(
            model_name='sensordata',
            name='temperature',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=6),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='sensor',
            name='mac',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]