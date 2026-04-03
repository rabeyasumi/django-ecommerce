import requests
from django.utils.text import slugify
from django.core.management import BaseCommand
from product.models import Category, Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        print('creating data.......')

        response = requests.get('https://dummyjson.com/products').json()

        for product in response['products']:
            try:
                print("Processing:", product['title'])

                category, _ = Category.objects.get_or_create(
                    title=product['category'],
                    slug=slugify(product['category'])
                )

                slug = slugify(product['title']) + f"-{product['id']}"

                obj, created = Product.objects.get_or_create(
                    slug=slug,
                    defaults={
                        'category': category,
                        'title': product['title'],
                        'price': product['price'],
                        'thumbnail': product.get('thumbnail', ''),
                        'description': product.get('description', ''),
                    }
                )

                if created:
                    print("Created:", obj.title)
                else:
                    print("Exists:", obj.title)

            except Exception as e:
                print("ERROR:", e)

        print("insertion complete!")