# Generated by Django 4.1.7 on 2023-03-21 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipes',
            name='recipe_image',
            field=models.ImageField(default='recipes/placeholder.png', upload_to='recipes/'),
        ),
    ]
