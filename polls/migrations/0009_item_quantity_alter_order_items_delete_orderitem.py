# Generated by Django 4.0 on 2022-08-23 00:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0008_item_colour_alter_item_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='order',
            name='items',
            field=models.ManyToManyField(to='polls.Item'),
        ),
        migrations.DeleteModel(
            name='OrderItem',
        ),
    ]
