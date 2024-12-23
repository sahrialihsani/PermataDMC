# Generated by Django 3.2.25 on 2024-12-23 12:08

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('tourism', '0002_auto_20241223_1820'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed To Transaction'), ('cancelled', 'Cancelled')], default='pending', max_length=20),
        ),
        migrations.AlterField(
            model_name='article',
            name='tanggal_post',
            field=models.DateTimeField(default=datetime.datetime(2024, 12, 23, 12, 8, 53, 386331, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='transaksi',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 12, 23, 12, 8, 53, 386331, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='transaksi',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 12, 23, 12, 8, 53, 386331, tzinfo=utc)),
        ),
    ]