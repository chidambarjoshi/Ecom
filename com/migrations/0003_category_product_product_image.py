# Generated by Django 3.2 on 2021-05-05 05:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('com', '0002_users_password2'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cat_name', models.CharField(max_length=20, unique=True)),
                ('cat_image', models.ImageField(upload_to='category')),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=50)),
                ('price', models.DecimalField(decimal_places=2, max_digits=9)),
                ('description', models.CharField(blank=True, max_length=150, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='com.category')),
            ],
        ),
        migrations.CreateModel(
            name='product_image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='product')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='com.product')),
            ],
        ),
    ]
