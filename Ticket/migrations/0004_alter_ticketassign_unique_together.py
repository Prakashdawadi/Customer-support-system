# Generated by Django 3.2.7 on 2021-10-08 10:53

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Ticket', '0003_alter_ticketassign_table'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='ticketassign',
            unique_together={('ticketId', 'caretakerId', 'customerId')},
        ),
    ]
