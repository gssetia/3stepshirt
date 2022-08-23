# Generated by Django 4.0 on 2022-08-22 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0006_alter_item_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='size',
            field=models.CharField(choices=[('XS', 'Extra Small'), ('S', 'Small'), ('M', 'Medium'), ('L', 'L'), ('Large', 'Extra Large')], max_length=5),
        ),
    ]
