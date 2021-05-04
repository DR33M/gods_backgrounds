# Generated by Django 3.1.8 on 2021-05-03 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20210503_1747'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='extension',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='image',
            name='height',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='image',
            name='ratio',
            field=models.FloatField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='image',
            name='width',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]