# Generated by Django 3.2.25 on 2024-12-23 11:20

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('tourism', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='tanggal_post',
            field=models.DateTimeField(default=datetime.datetime(2024, 12, 23, 11, 20, 30, 966898, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='transaksi',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 12, 23, 11, 20, 30, 966898, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='transaksi',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 12, 23, 11, 20, 30, 966898, tzinfo=utc)),
        ),
    ]
