# Generated by Django 2.1.7 on 2019-03-06 18:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_order_shipping_fee'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='sub_total',
        ),
    ]
