# Generated by Django 3.1.7 on 2021-04-16 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20210411_1501'),
    ]

    operations = [
        migrations.AddField(
            model_name='colors',
            name='similar_color',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]