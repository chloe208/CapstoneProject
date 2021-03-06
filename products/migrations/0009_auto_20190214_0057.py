# Generated by Django 2.1.7 on 2019-02-14 05:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_auto_20190214_0055'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productimage',
            name='shade',
        ),
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=models.ImageField(default=1, upload_to='products/images/'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='variation',
            name='image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.ProductImage'),
        ),
    ]
