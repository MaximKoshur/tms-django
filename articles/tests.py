from django.test import TestCase
from django.urls import reverse
from .models import Article


class ArticlesIndexViewTest(TestCase):
    def test_no_articles(self):
        response = self.client.get(reverse('articles:articles'))
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, 'No articles are available')

    def check_all_articles_index(self):
        context_test = Article.objects.all()
        response = self.client.get(reverse('articles:articles'))
        self.assertEquals(response.status_code, 200)
        self.assertQuerysetEqual(response.context['context'], [context_test])


class ArticlesDetailViewTest(TestCase):
    def setUp(self):
        Article.objects.create(id=1, text='Test Article Text', name='Text', author='Text', like_count=0)

    def test_no_article_404(self):
        article_id = 1000
        response = self.client.get(reverse('articles:articles_id', args=[article_id]))
        self.assertEquals(response.status_code, 404)

    def test_equal_article(self):
        context = Article.objects.get(id=1).text
        article_id = 1
        response = self.client.get(reverse('articles:articles_id', args=[article_id]))
        self.assertEquals(response.status_code, 200)
        self.assertEqual(response.context['context'].text, context)


class ArticlesPopularTest(TestCase):
    def setUp(self):
        Article.objects.create(id=1, text='Test Article Text', name='Text', author='Text', like_count=3)
        Article.objects.create(id=2, text='Test Article Text', name='Text', author='Text', like_count=1000)

    def test_is_it_popular(self):
        context = Article.objects.get(id=1)
        article = context.is_popular()
        self.assertEqual(False, article)

    def test_is_it_unpopular(self):
        context = Article.objects.get(id=2)
        article = context.is_popular()
        self.assertEqual(True, article)


