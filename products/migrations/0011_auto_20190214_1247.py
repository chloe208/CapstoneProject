# Generated by Django 2.1.7 on 2019-02-14 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_variation_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variation',
            name='category',
            field=models.CharField(choices=[('shade', 'shade'), ('package', 'package'), ('size', 'size')], default='shade', max_length=120),
        ),
    ]