from django.core.management import BaseCommand
from shop.models import Category, Product
from django.utils import timezone
import json


class Command(BaseCommand):
    help = 'Hi'

    def add_arguments(self, parser):
        parser.add_argument('--data_file_path', type=str, required=False, default="shop/data.json")

    def handle(self, *args, **options):
        Category.objects.all().delete()
        Product.objects.all().delete()
        file = options['data_file_path']
        with open(file) as f:
            file_content = f.read()
            templates = json.loads(file_content)
        for i in templates:
            c = Category.objects.create(name=i)
            for j in templates[i]:
                p = Product.objects.create(category=c, name=templates[i][j].get('name'), description=templates[i][j].get('description'), price=templates[i][j].get('price'))

    # populate_polls_database('data.json')
