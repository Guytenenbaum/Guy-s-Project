# Generated by Django 4.1.7 on 2023-04-22 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Clients', '0002_rename_user_id_cart_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='delivery',
            name='total_price',
            field=models.IntegerField(default=0),
        ),
    ]
