# Generated by Django 5.0 on 2024-02-02 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0005_remove_author_article'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='author',
            field=models.ManyToManyField(to='articles.author'),
        ),
    ]
