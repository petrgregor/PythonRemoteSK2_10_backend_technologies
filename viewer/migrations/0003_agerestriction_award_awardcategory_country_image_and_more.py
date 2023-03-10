# Generated by Django 4.1.1 on 2023-01-27 18:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('viewer', '0002_movie'),
    ]

    operations = [
        migrations.CreateModel(
            name='AgeRestriction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Award',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('year', models.IntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-year', 'category'],
            },
        ),
        migrations.CreateModel(
            name='AwardCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=64)),
                ('description', models.CharField(max_length=128, null=True)),
            ],
        ),
        migrations.AlterModelOptions(
            name='movie',
            options={'ordering': ['title_orig']},
        ),
        migrations.RemoveField(
            model_name='movie',
            name='rating',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='title',
        ),
        migrations.AddField(
            model_name='movie',
            name='earnings',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='expanses',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='length',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='link',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=6, null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='title_cz',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='title_orig',
            field=models.CharField(default='No title set', max_length=64),
        ),
        migrations.AddField(
            model_name='movie',
            name='title_sk',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='trailer',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='genre',
            name='name',
            field=models.CharField(max_length=16, unique=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='genre',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='viewer.genre'),
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16, null=True)),
                ('surname', models.CharField(max_length=16, null=True)),
                ('artist_name', models.CharField(max_length=16, null=True)),
                ('date_of_birth', models.DateField(null=True)),
                ('death_date', models.DateField(null=True)),
                ('biography', models.TextField(null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('acting', models.ManyToManyField(related_name='acting_in_movie', to='viewer.movie')),
                ('awards', models.ManyToManyField(to='viewer.award')),
                ('country', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='viewer.country')),
                ('directing', models.ManyToManyField(related_name='directing_movie', to='viewer.movie')),
            ],
            options={
                'ordering': ['surname', 'artist_name', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveSmallIntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='viewer.movie')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['movie', 'created'],
            },
        ),
        migrations.AddField(
            model_name='award',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='viewer.awardcategory'),
        ),
        migrations.AddField(
            model_name='award',
            name='movie',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='viewer.movie'),
        ),
        migrations.AddField(
            model_name='movie',
            name='age_restriction',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='viewer.agerestriction'),
        ),
        migrations.AddField(
            model_name='movie',
            name='country',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='viewer.country'),
        ),
        migrations.AddField(
            model_name='movie',
            name='images',
            field=models.ManyToManyField(to='viewer.image'),
        ),
    ]
