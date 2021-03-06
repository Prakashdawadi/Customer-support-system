# Generated by Django 3.2.7 on 2021-10-11 11:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Ticket', '0016_auto_20211010_2019'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ticketconversation',
            options={'ordering': ['created_at']},
        ),
        migrations.AddField(
            model_name='ticketconversation',
            name='msg_created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='msg_id', to=settings.AUTH_USER_MODEL),
        ),
    ]
