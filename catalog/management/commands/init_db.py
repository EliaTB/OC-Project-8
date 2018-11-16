from django.core.management.base import BaseCommand, CommandError
from catalog.models import Category, Product


class Command(BaseCommand):
	help = 'Initializes the database'

	CATEGORIES =  ['charcuteries', 'chocolats', 'pates-a-tartiner', 'biscuits', 
				'boissons', 'yaourts', 'pains', 'glace', 'fromages-de-france']

	def create_db(self):

		for category in self.CATEGORIES
			new_category = Category(name=category)
			new_category.save()


			params = {
			        'json': 1,
			        'page_size': 100,
			        'page': 1,
			        'tagtype_0': 'categories',
		            'tag_contains_0': 'contains',
		            'tag_0': category,
			        }

			response = get('https://fr.openfoodfacts.org/cgi/search.pl',
			                params=params)
			data = response.json()
			products = data['products']

			for element in products:
				try:

					product_new = Product(name=element["product_name"], brand=element["brand"], nutrition_grade=element["nutrition_grade_fr"], 
									url=element["url"], picture=element['image_url'], nutrition_image=element["image_nutrition_small_url"], 
									category=new_category)
					product_new.save()

					except KeyError: 
		                pass
		            except connexion.OperationalError: #Don't take the products with encoding error
		                pass
		            except connexion.DataError: #Pass when product name is too long
		                pass

	def handle(self, *args, **options):
        self.create_db()
