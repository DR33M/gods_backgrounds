# Generated by Django 3.1.10 on 2021-05-16 12:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taggit', '0003_taggeditem_add_unique_index'),
    ]

    operations = [
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hex', models.CharField(max_length=7, unique=True)),
                ('similar_color', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'verbose_name_plural': 'Colors',
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=50)),
                ('image', models.ImageField(upload_to='images/%Y/%m/%d/full_size/')),
                ('preview_image', models.ImageField(blank=True, upload_to='images/%Y/%m/%d/preview_size/')),
                ('image_hash', models.CharField(blank=True, max_length=255)),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True)),
                ('rating', models.IntegerField(blank=True, default=0)),
                ('downloads', models.IntegerField(blank=True, default=0)),
                ('width', models.IntegerField(blank=True, default=0)),
                ('height', models.IntegerField(blank=True, default=0)),
                ('ratio', models.FloatField(blank=True, default=0)),
                ('size', models.CharField(blank=True, max_length=255)),
                ('extension', models.CharField(blank=True, max_length=255)),
                ('status', models.IntegerField(choices=[(0, 'Moderation'), (1, 'Approved')], default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('colors', models.ManyToManyField(blank=True, to='main.Color')),
                ('moderator', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='moderator_id', to=settings.AUTH_USER_MODEL)),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
        ),
        migrations.CreateModel(
            name='UsersActions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote', models.IntegerField(choices=[(-1, 'Downvote'), (0, 'Default'), (1, 'Upvote')], default=0)),
                ('downloaded', models.BooleanField(default=False)),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.image')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('body', models.TextField()),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.image')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
