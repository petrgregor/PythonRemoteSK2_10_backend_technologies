# Generated by Django 4.1.1 on 2023-01-27 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0005_alter_movie_age_restriction_alter_movie_earnings_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='country',
        ),
        migrations.AddField(
            model_name='movie',
            name='country',
            field=models.ManyToManyField(to='viewer.country'),
        ),
    ]
