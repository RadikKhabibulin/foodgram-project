# Generated by Django 3.1 on 2021-04-19 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0005_auto_20210420_0043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='ingredient',
            field=models.ManyToManyField(blank=True, related_name='recipes', through='recipes.Composition', to='recipes.Ingredient'),
        ),
    ]
