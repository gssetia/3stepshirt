# Generated by Django 4.0 on 2022-08-25 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0013_order_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='colour',
            field=models.CharField(choices=[('wht', 'White'), ('red', 'Red'), ('blk', 'Black')], max_length=3),
        ),
    ]
