# Generated by Django 3.2.7 on 2021-10-09 14:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Ticket', '0008_auto_20211009_1817'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='assigned_to',
        ),
        migrations.AlterField(
            model_name='ticket',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]