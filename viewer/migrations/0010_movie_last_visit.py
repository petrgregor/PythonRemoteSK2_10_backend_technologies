# Generated by Django 4.1.1 on 2023-02-06 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0009_alter_genre_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='last_visit',
            field=models.DateTimeField(null=True),
        ),
    ]
