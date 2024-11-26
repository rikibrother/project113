# Generated by Django 5.1.2 on 2024-11-09 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_extended'),
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('year', models.CharField(max_length=4, null=True)),
                ('rated', models.CharField(max_length=10, null=True)),
                ('released', models.DateField(null=True)),
                ('runtime', models.CharField(max_length=50, null=True)),
                ('genre', models.CharField(max_length=255, null=True)),
                ('director', models.CharField(max_length=255, null=True)),
                ('writer', models.CharField(max_length=255, null=True)),
                ('actors', models.TextField(null=True)),
                ('plot', models.TextField(null=True)),
                ('language', models.CharField(max_length=255, null=True)),
                ('country', models.CharField(max_length=255, null=True)),
                ('awards', models.CharField(max_length=255, null=True)),
                ('poster', models.URLField(null=True)),
                ('metascore', models.IntegerField(null=True)),
                ('imdb_rating', models.FloatField(null=True)),
                ('imdb_votes', models.CharField(max_length=20, null=True)),
                ('imdb_id', models.CharField(max_length=20, null=True)),
                ('type', models.CharField(max_length=50, null=True)),
                ('response', models.BooleanField(default=True)),
            ],
        ),
    ]
