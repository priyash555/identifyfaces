# Generated by Django 3.0.3 on 2020-12-21 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_auto_20201221_2356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testimages',
            name='ResultImage',
            field=models.ImageField(blank=True, upload_to='test'),
        ),
    ]
