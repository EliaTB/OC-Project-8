from django.test import TestCase, client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.management import call_command
from io import StringIO
from .models import Product, Category, UserFavorite

# Create your tests here.

class IndexPageTestCase(TestCase):

    def test_index_returns_200(self):
        response = self.client.get(reverse('catalog:index'))
        self.assertEqual(response.status_code, 200)



class UserViewTests(TestCase):


	def setUp(self):
		user = User.objects.create(username='testuser', password="password")


	def test_login(self):
		response = self.client.post(reverse('login'),
									{'username': 'testuser',
									'password': 'password'}, follow=True)
		self.assertEqual(response.status_code, 200)


	def test_register(self):
		response = self.client.post(reverse('register'),
									{'username': 'test',
									'email': 'testuser@email.com',
									'password1': 'password',
									'password2' : 'password' }, follow=True)
		self.assertEqual(response.status_code, 200)

	def test_logout(self):

		self.client.login(username='testuser', password='password')
		self.client.logout()
		self.assertRaises(KeyError, lambda: self.client.session['_auth_user_id'])



class DataTests(TestCase):

	def setUp(self):
		pizzas = Category.objects.create(name='pizzas')

		Product.objects.create(name='Pizza',
        					category=pizzas,
                            brand='casino',
                            nutrition_grade='a',                            
                            picture='www.pizzajpeg.com',
        					nutrition_image='www.pizzanutrigrade.com',
                            url='www.pizza.com')


	def test_search_returns_200(self):
		Pizza = str('Pizza')
		response = self.client.get(reverse('catalog:search'), {
			'query': Pizza,
		})
		self.assertEqual(response.status_code, 200)

	def test_search_page_redirect_302(self):
		Pizza = str('invalid name')
		response = self.client.get(reverse('catalog:search'), {
			'query': Pizza,
		})
		self.assertEqual(response.status_code, 302)


class CommandTestCase(TestCase):

    def test_populate_db_command(self):

        out = StringIO()
        call_command('init_db', stdout=out)
        self.assertIn('', out.getvalue())