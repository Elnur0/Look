# Generated by Django 4.2.4 on 2024-01-17 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0013_category_name_az_category_name_en_category_parent_az_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='aditional_info',
            field=models.TextField(blank=True, null=True),
        ),
    ]
