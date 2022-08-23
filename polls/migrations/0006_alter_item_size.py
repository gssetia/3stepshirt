# Generated by Django 4.0 on 2022-08-22 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_remove_item_slug_alter_item_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='size',
            field=models.CharField(choices=[('XS', 'Extra Small'), ('S', 'Small'), ('M', 'Medium'), ('L', 'Large'), ('Large', 'Extra Large')], max_length=5),
        ),
    ]