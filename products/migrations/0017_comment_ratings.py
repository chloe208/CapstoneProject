# Generated by Django 2.1.7 on 2019-03-19 02:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0016_merge_20190318_1937'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='ratings',
            field=models.CharField(choices=[('5', '5'), ('4', '4'), ('3', '3'), ('2', '2'), ('1', '1')], default='5', max_length=120),
        ),
    ]