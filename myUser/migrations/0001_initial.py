# Generated by Django 3.2.7 on 2021-10-04 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email')),
                ('name', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=60)),
                ('phone_no', models.CharField(max_length=16)),
                ('image', models.ImageField(upload_to='user/')),
                ('status', models.CharField(choices=[('available', 'available'), ('busy', 'busy')], max_length=9)),
                ('is_customer', models.BooleanField(default=False)),
                ('is_Caretaker', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]