# Generated by Django 2.1.7 on 2019-02-14 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_auto_20190214_1247'),
        ('carts', '0004_cartitem_notes'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='variations',
            field=models.ManyToManyField(blank=True, null=True, to='products.Variation'),
        ),
    ]
