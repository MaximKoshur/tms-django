from django.db import models
from django.utils import timezone
from django.db.models import signals


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField(verbose_name="date published")

    class MyModels(models.Model):
        my_field = models.CharField(max_length=100, db_index=True)

    def was_published_recently(self):
        now = timezone.now()
        return now - timezone.timedelta(days=1) <= self.pub_date

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.question.question_text} - {self.choice_text}'


def my_callback(sender, *args, **kwargs):
    print(f'Pre init. Sender: {sender}, args: {args}, kwargs: {kwargs}')


signals.pre_init.connect(my_callback, sender=Question)


class BaseUser(models.Model):
    username = models.CharField(max_length=100)

    class Meta:
        abstract = True

class Manager(BaseUser):
    project = models.CharField(max_length=100)

class Engineer(BaseUser):
    language = models.CharField(max_length=100)


#Question.object.bulk_create([Question(question_text='1',pub_date=timezone.now()),Question(question_text='2',pub_date=timezone.now()),])