from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doc', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='image',
            field=models.ImageField(default='', upload_to=''),
        ),
    ]
