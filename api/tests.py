from django.test import TestCase
from django.utils import timezone
from polls.models import Question, Choice
from shop.models import Product, Category
from articles.models import Article


class QuestionViewTest(TestCase):
    def test_empty_question_list(self):
        response = self.client.get('/api/questions/')
        self.assertEquals(response.status_code, 200)

        data = response.json()
        self.assertEquals(data, {'count': 0, 'next': None, 'previous': None, 'results': []})

    def test_question_list(self):
        Question.objects.create(question_text='Text1', pub_date=timezone.now())
        Question.objects.create(question_text='Text2', pub_date=timezone.now())

        response = self.client.get('/api/questions/')
        self.assertEquals(response.status_code, 200)

        data = response.json()
        self.assertEquals(len(data), 4)
        self.assertEquals(data['results'][0]['question_text'], 'Text1')
        self.assertEquals(data['results'][1]['question_text'], 'Text2')

    def test_nonexistent_question_detail(self):
        response = self.client.get('/api/questions/1/')
        self.assertEquals(response.status_code, 404)

    def test_question_detail(self):
        question = Question.objects.create(question_text='Text1', pub_date=timezone.now())

        response = self.client.get(f'/api/questions/{question.id}/')
        self.assertEquals(response.status_code, 200)

        data = response.json()
        self.assertEquals(data['question_text'], question.question_text)


class ArticlesViewTest(TestCase):
    def test_empty_article_list(self):
        response = self.client.get('/api/articles/')
        self.assertEquals(response.status_code, 200)
        data = response.json()
        self.assertEquals(data, {'count': 0, 'next': None, 'previous': None, 'results': []})

    def test_nonexistent_article_detail(self):
        response = self.client.get('/api/articles/1/')
        self.assertEquals(response.status_code, 404)

    def test_article_detail(self):
        article = Article.objects.create(name='abc', text='abc', like_count=5)

        response = self.client.get(f'/api/articles/{article.id}/')
        self.assertEquals(response.status_code, 200)

        data = response.json()
        self.assertEquals(data['name'], article.name)


class ProductViewTest(TestCase):
    def test_empty_product_list(self):
        response = self.client.get('/api/product/')
        self.assertEquals(response.status_code, 200)
        data = response.json()
        self.assertEquals(data, {'count': 0, 'next': None, 'previous': None, 'results': []})

    def test_nonexistent_product_detail(self):
        response = self.client.get('/api/product/1/')
        self.assertEquals(response.status_code, 404)

    def test_product_detail(self):
        category = Category.objects.create(name="Food")
        product = Product.objects.create(name='abc', price=5, description='abc', category=category)

        response = self.client.get(f'/api/product/{product.id}/')
        self.assertEquals(response.status_code, 200)

        data = response.json()
        self.assertEquals(data['name'], product.name)


class CategoryViewTest(TestCase):
    def test_empty_category_list(self):
        response = self.client.get('/api/category/')
        self.assertEquals(response.status_code, 200)
        data = response.json()
        self.assertEquals(data, {'count': 0, 'next': None, 'previous': None, 'results': []})

    def test_nonexistent_category_detail(self):
        response = self.client.get('/api/category/1/')
        self.assertEquals(response.status_code, 404)

    def test_category_detail(self):
        category = Category.objects.create(name="Food")

        response = self.client.get(f'/api/category/{category.id}/')
        self.assertEquals(response.status_code, 200)

        data = response.json()
        self.assertEquals(data['name'], category.name)


class ChoiceViewTest(TestCase):
    def test_empty_choice_list(self):
        response = self.client.get('/api/choices/')
        self.assertEquals(response.status_code, 200)
        data = response.json()
        self.assertEquals(data, {'count': 0, 'next': None, 'previous': None, 'results': []})

    def test_nonexistent_choice_detail(self):
        response = self.client.get('/api/choices/1/')
        self.assertEquals(response.status_code, 404)

    def test_choice_detail(self):
        question = Question.objects.create(question_text='Text1', pub_date=timezone.now())
        choice = Choice.objects.create(choice_text='abc', votes=9, question=question)

        response = self.client.get(f'/api/choices/{choice.id}/')
        self.assertEquals(response.status_code, 200)

        data = response.json()
        self.assertEquals(data['choice_text'], choice.choice_text)


