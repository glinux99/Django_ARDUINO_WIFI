# Generated by Django 2.2.24 on 2021-10-13 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gateway', '0006_auto_20211013_1237'),
    ]

    operations = [
        migrations.DeleteModel(
            name='alarme',
        ),
        migrations.AddField(
            model_name='autorisation',
            name='alarme_on',
            field=models.BooleanField(null=True),
        ),
    ]
