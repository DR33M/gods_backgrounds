# Generated by Django 3.1.8 on 2021-05-03 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20210503_1738'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='height',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='image',
            name='width',
            field=models.IntegerField(default=0),
        ),
    ]