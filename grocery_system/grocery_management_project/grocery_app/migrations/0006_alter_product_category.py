# Generated by Django 4.2.15 on 2024-08-21 12:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('grocery_app', '0005_product_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(default='fruits', on_delete=django.db.models.deletion.CASCADE, to='grocery_app.category'),
        ),
    ]