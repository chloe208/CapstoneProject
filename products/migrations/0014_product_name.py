# Generated by Django 2.1.7 on 2019-03-18 23:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0013_auto_20190318_1311'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='name',
            field=models.CharField(default=1, max_length=120),
            preserve_default=False,
        ),
    ]
