# Generated by Django 4.2.4 on 2023-09-28 17:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_alter_product_sku'),
    ]

    operations = [
        migrations.RenameField(
            model_name='color',
            old_name='kod',
            new_name='code',
        ),
    ]
