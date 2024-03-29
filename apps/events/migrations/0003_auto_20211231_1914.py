# Generated by Django 3.1.5 on 2021-12-31 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20200708_0034'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='teaser_link',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='summary',
            field=models.TextField(blank=True, null=True),
        ),
    ]
