# Generated by Django 2.2.11 on 2020-06-27 23:18

from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EmailText',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=100)),
                ('text', models.TextField(max_length=1000)),
                ('link', models.CharField(blank=True, max_length=400, null=True)),
                ('link_text', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('date_joint', models.DateTimeField(default=django.utils.timezone.now)),
                ('unique_id', models.UUIDField(default=uuid.uuid4, editable=False)),
            ],
        ),
    ]
