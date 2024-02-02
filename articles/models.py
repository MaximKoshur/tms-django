from django.db import models
from django.contrib import admin


class Article(models.Model):
    name = models.CharField(max_length=200)
    text = models.CharField(max_length=1000)
    like_count = models.IntegerField(default=0)
    author = models.ManyToManyField('Author')

    @admin.display(
        boolean=True,
        description='Is popular?'
    )
    def is_popular(self):
        return self.like_count >= 100

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Article'


class Author(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    date_of_birth = models.CharField(max_length=1000)


