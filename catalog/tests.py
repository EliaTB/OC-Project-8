from django.test import TestCase, client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Product, Category, UserFavorite

# Create your tests here.

class StatutsViewTests(TestCase):


	def setUp(self):
		user = User.objects.create(username='testuser', password="password")

	def test_index(self):
		response = self.client.get(reverse('catalog:index'))
		self.assertEqual(response.status_code, 200)

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

	def test_search(self):
		response = self.client.post(reverse('catalog:search'),
								{'search': 'Nutella'})
		self.assertEqual(response.status_code, 200)