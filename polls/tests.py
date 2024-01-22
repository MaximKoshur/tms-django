from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .models import Question
from django.db import transaction


def create_questions(text, days):
    pub_date = timezone.now() + timezone.timedelta(days=days)
    return Question.objects.create(question_text=text, pub_date=pub_date)

# @transaction.atomic
# def create_questions(raising):
#    Question.objects.create(pub_date=timezone.now())
#    if raising:
#        raise Exception()
#    Question.objects.create(pub_date=timezone.now())


class QuestionIndexViewTest(TestCase):
    def test_no_questions(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, 'No polls are available')

    def test_future_question_and_post_questions(self):
        past_question = create_questions('past', -30)
        create_questions('future', 30)
        response = self.client.get(reverse('polls:index'))
        self.assertEquals(response.status_code, 200)
        self.assertQuerysetEqual(response.context['latest_question_list'], [past_question])

    def test_old_questions_was_not_published_recently(self):
        pub_date = timezone.now() - timezone.timedelta(days=2)
        question = Question(pub_date=pub_date)
        self.assertFalse(question.was_published_recently())

    def test_new_questions_was_not_published_recently(self):
        pub_date = timezone.now() - timezone.timedelta(hours=12)
        question = Question(pub_date=pub_date)
        self.assertTrue(question.was_published_recently())


class TestTransaction(TestCase):
    def test_transaction(self):
        self.assertEqual(Question.objects.count(), 0)
        create_questions(False)
        self.assertEqual(Question.objects.count(), 2)
        self.assertRaises(Exception, lambda: create_questions(True))

        # check question count is still 2
        self.assertEqual(Question.objects.count(), 2)
