# Generated by Django 3.2.7 on 2021-10-07 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Category', '0002_auto_20211007_1426'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='status',
            field=models.CharField(choices=[('active', 'active'), ('inactive', 'inactive')], default='active', max_length=8),
        ),
    ]
