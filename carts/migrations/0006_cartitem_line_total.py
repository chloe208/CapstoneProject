# Generated by Django 2.1.7 on 2019-02-14 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0005_cartitem_variations'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='line_total',
            field=models.DecimalField(decimal_places=2, default=10.99, max_digits=1000),
        ),
    ]
