# Generated by Django 2.1.7 on 2019-03-24 01:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0007_remove_cartitem_variations'),
        ('products', '0019_auto_20190323_2109'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='variation',
            name='image',
        ),
        migrations.RemoveField(
            model_name='variation',
            name='product',
        ),
        migrations.DeleteModel(
            name='Variation',
        ),
    ]
