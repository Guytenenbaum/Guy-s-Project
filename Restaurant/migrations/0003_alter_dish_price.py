# Generated by Django 4.1.7 on 2023-04-23 17:57

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Restaurant', '0002_rename_category_id_dish_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dish',
            name='price',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]