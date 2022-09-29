# Generated by Django 2.2.16 on 2022-09-29 16:22

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    replaces = [('reviews', '0003_auto_20220929_2016'), ('reviews', '0004_auto_20220929_2023'), ('reviews', '0005_auto_20220929_2024'), ('reviews', '0006_auto_20220929_2028'), ('reviews', '0007_auto_20220929_2030'), ('reviews', '0008_auto_20220929_2033'), ('reviews', '0009_auto_20220929_2106')]

    dependencies = [
        ('reviews', '0002_auto_20220926_2148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='date_joined',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='password',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='title',
            name='description',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.RemoveField(
            model_name='title',
            name='genre',
        ),
        migrations.CreateModel(
            name='GenreTitle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reviews.Genre')),
                ('title', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reviews.Title')),
            ],
        ),
        migrations.AddField(
            model_name='title',
            name='genre',
            field=models.ManyToManyField(blank=True, through='reviews.GenreTitle', to='reviews.Genre'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='password',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='date_joined',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='is_active',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='is_staff',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='is_superuser',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='confirmation_code',
            field=models.CharField(blank=True, max_length=555, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='token',
            field=models.CharField(blank=True, max_length=555, null=True),
        ),
        migrations.AlterField(
            model_name='title',
            name='description',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.RemoveField(
            model_name='title',
            name='review',
        ),
        migrations.AddField(
            model_name='review',
            name='title',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='reviews.Title'),
        ),
    ]
