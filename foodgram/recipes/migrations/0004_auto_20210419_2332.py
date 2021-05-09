# Generated by Django 3.1 on 2021-04-19 20:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_auto_20210419_2330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='composition',
            name='recipe',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='compositions', to='recipes.recipe'),
        ),
    ]
