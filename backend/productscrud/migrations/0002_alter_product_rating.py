# Generated by Django 5.1.3 on 2024-12-05 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productscrud', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='rating',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
