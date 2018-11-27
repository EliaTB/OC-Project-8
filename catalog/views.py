import requests
import json

from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from .models import Product, Category, UserFavorite
# Create your views here.


def index(request):
    return render(request, 'catalog/index.html')



def autocomplete(request):

	if request.is_ajax():
		query = request.GET.get('query')
		products = Product.objects.filter(name__icontains=query)
		results = []
		for p in products:
			product_dict = {}
			product_dict["name"] = p.name
			results.append(product_dict)
		data = json.dumps(results)
	else:
		data = 'fail'
	return HttpResponse(data, 'application/json')


def search(request):

    query = request.GET.get('query')
    
    product = Product.objects.get(name=query)
    product_cat = Product.objects.filter(category=product.category)

    context = {
        'tag': query,
    }

    # if ObjectDoesNotExist():
    # 	context['message'] = "Aucun produit a été trouvé "
    # 	context['link'] = "https://fr.openfoodfacts.org/cgi/search.pl?search_terms={}&search_simple=1&action=process".format(
    # 	query)

    substitutes = []
    for new_product in product_cat:
    	if new_product.nutrition_grade < product.nutrition_grade:
    		substitutes.append(new_product)


    paginator = Paginator(substitutes, 9)
    page = request.GET.get('page')
    alt_products = paginator.get_page(page)


    context['alt_products'] = alt_products
    context['paginate'] = True
   


    return render(request, 'catalog/search.html', context)


def product_detail(request, product_id):
    
    product = Product.objects.get(id=product_id)

    context = {
        'name': product.name,
        'title': 'Informations nutritionnelles',
        'product': product,
        'nutrition_image': product.nutrition_image,
    }

    return render(request, 'catalog/product_detail.html', context)



@login_required
def add_favorite(request, product_id):
    try:
        UserFavorite.objects.get(user_name_id=request.user.id, product_id=(product_id))
        message = "Ce produit est déjà dans vos favoris."
    except ObjectDoesNotExist:
        UserFavorite.objects.create(user_name_id=request.user.id, product_id=(product_id))
        message = "Le produit a bien été enregistré."

    return HttpResponse(message)

