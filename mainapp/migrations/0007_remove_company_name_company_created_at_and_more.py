# Generated by Django 4.2.4 on 2023-10-03 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0006_rename_kupon_company_coupon_company_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='name',
        ),
        migrations.AddField(
            model_name='company',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default='2023-12-12'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='company',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]