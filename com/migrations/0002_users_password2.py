# Generated by Django 3.2 on 2021-05-04 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('com', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='password2',
            field=models.CharField(blank=True, max_length=15, null=True, unique=True),
        ),
    ]