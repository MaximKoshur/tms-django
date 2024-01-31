from django.db import models


class Article(models.Model):
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    text = models.CharField(max_length=1000)
    like_count = models.IntegerField(default=0)

    def is_popular(self):
        return self.like_count >= 100


