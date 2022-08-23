# Generated by Django 4.0 on 2022-08-23 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0011_alter_item_colour'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='1',
            new_name='user',
        ),
        migrations.AlterField(
            model_name='item',
            name='colour',
            field=models.CharField(choices=[('red', 'Red'), ('wht', 'White'), ('blk', 'Black')], max_length=3),
        ),
    ]
