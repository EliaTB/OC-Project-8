import requests
import json

from django.shortcuts import render, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages

from .models import Product, Category, UserFavorite
# Create your views here.


def index(request):
    return render(request, 'catalog/index.html')



def autocomplete(request):

	if request.is_ajax():
		query = request.GET.get('term', '')
		products = Product.objects.filter(name__icontains=query).order_by("-nutrition_grade")[:10]
		results = []
		for p in products:
			product_dict = {}
			product_dict = p.name
			results.append(product_dict)
		data = json.dumps(results)
	else:
		data = 'fail'
	return HttpResponse(data, 'application/json')



def search(request):

    query = request.GET.get('query')
    
    product = Product.objects.filter(name=query).first()
    substitutes = Product.objects.filter(category=product.category, nutrition_grade__lt=product.nutrition_grade).order_by("nutrition_grade")

    # if ObjectDoesNotExist():
    # 	context['message'] = "Aucun produit a été trouvé "
    # 	context['link'] = "https://fr.openfoodfacts.org/cgi/search.pl?search_terms={}&search_simple=1&action=process".format(
    # 	query)

    # substitutes = []
    # for new_product in product_cat:
    # 	if new_product.nutrition_grade < product.nutrition_grade:
    # substitutes.append(new_product)


    paginator = Paginator(substitutes, 6)
    page = request.GET.get('page')
    alt_products = paginator.get_page(page)

    context = {
    	'alt_products': alt_products,
    	'paginate': True,
        'title': query,
        'og_id': product.id
    }

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
def add_favorite(request, product_id, og_product_id):
    try:
        UserFavorite.objects.get(user_name_id=request.user.id, product_id=(product_id), original_product_id=(og_product_id))
        messages.warning(request, f'Ce produit est déjà dans vos favoris.')
        return redirect(request.META.get('HTTP_REFERER'))
    except ObjectDoesNotExist:
        UserFavorite.objects.create(user_name_id=request.user.id, product_id=(product_id), original_product_id=(og_product_id))
        messages.success(request, f'Le produit a bien été enregistré.')
        return redirect(request.META.get('HTTP_REFERER'))




