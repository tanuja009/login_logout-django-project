# Generated by Django 4.2.15 on 2024-08-21 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grocery_app', '0003_product_carousal_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
    ]