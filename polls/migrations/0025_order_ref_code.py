# Generated by Django 4.0 on 2022-08-28 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0024_rename_processing_order_delivering_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='ref_code',
            field=models.CharField(default='123', max_length=20),
            preserve_default=False,
        ),
    ]
