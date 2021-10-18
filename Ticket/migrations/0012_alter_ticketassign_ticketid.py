# Generated by Django 3.2.7 on 2021-10-10 04:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Ticket', '0011_auto_20211010_0905'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticketassign',
            name='ticketId',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assignTicketId', to='Ticket.ticket'),
        ),
    ]