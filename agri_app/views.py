from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import *
from django.db.models import Max,Min,Count,Avg
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.core.paginator import Paginator


#Home
def home (request):
    data=Category.objects.all().order_by('-id')
    products =Product.objects.all().order_by('-id')[:8]
    total_data=Product.objects.all().count()

    # Count=Product.objects.annotate(items_count=Count('related_name_to_items'))
    return render (request, "index.html", {'data':data, 'products':products, 'total':total_data})

#Product_details
def product_details(request):
    return render (request, "product-details.html")

#Brand
def brand_list(request):
    data=Brand.objects.all().order_by('-id')
    return render(request, 'brand.html', {'data':data})


#Categories
def category_list(request):
    data=Category.objects.all().order_by('-id')
    products =Product.objects.all().order_by('-id')
    total_data=Product.objects.count()


    return render(request, 'category_list.html',{'data':data, 'products':products, 'total_data':total_data})

#Product List According to Category
def category_product_list(request,cat_id):
	category=Category.objects.get(id=cat_id)
	data=Product.objects.filter(category=category).order_by('-id')
	return render(request,'category_product_list.html',{
			'data':data,
			})

#All Category by filter from Nav
# def all_category(request,cat_id):
#     cat_data=Category.objects.all().order_by('-id')
#     product_data=Product.objects.filter(category=cat_data).order_by('-id')
#     return render(request, 'all_category.html', {'product_data',product_data})

#Product list acoording to brand               
def brand_product_list(request, brand_id):
    brand=Brand.objects.get(id=brand_id)
    data=Product.objects.filter(brand=brand).order_by('-id')
    # cats = Product.objects.distinct().values('category__title','category__image', 'category__id')
    # brands=Product.objects.distinct().values('brand__title','brand__id')
    min_price=ProductAttribute.objects.aggregate(Min('price'))
    max_price=ProductAttribute.objects.aggregate(Max('price'))
    return render (request, 'brand_product.html',
                  {'data':data,
                #    'cats':cats,
                #    'brands':brands,
                   'min_price':min_price,
                   'max_price':max_price
                   }
                   )

#Product Details
def product_detail(request, slug, id):
    product=Product.objects.get(id=id)
    related_products=Product.objects.filter(category=product.category).exclude(id=id)[:4]
    return render (request, 'product-details.html', {'data':product, 'related':related_products})

#About us
def about (request):
    return render (request, "about.html")

#Product view
# def product_list(request):
    

def contact (request):
    return render (request, "contact.html")

def blog (request):
    return render (request, "blog.html")

def shop (request):
    total_data=Product.objects.count()
    data=Product.objects.all().order_by('-id')
    # cats = Product.objects.distinct().values('category__title','category__image', 'category__id')
    # brands=Product.objects.distinct().values('brand__title','brand__id')
    # min_price=ProductAttribute.objects.aggregate(Min('price'))
    # max_price=ProductAttribute.objects.aggregate(Max('price'))
    # object_list =Product.objects.all().order_by('-id')

    # paginator = Paginator(object_list, 2)  # Show 2 objects per page

    # page = request.GET.get('page')
    # objects = paginator.get_page(page)

   
    
    return render (request, "shop.html", 
        {
            'data':data,
            # 'cats':cats,
            # 'brands':brands,
            'total_data':total_data,
            # 'min_price':min_price,
            # 'max_price':max_price,
            # 'objects': objects
        }  
        
        )

# Search
def search(request):
    q=request.GET['q']
    data=Product.objects.filter(title__icontains=q).order_by('-id') 
    data_class=Product.objects.all().order_by('-id')[:6]
    min_price=ProductAttribute.objects.aggregate(Min('price'))
    max_price=ProductAttribute.objects.aggregate(Max('price'))  
    return render(request,'search.html', 
                {'data':data,
                'data_class':data_class,
                'min_price':min_price,
                'max_price':max_price,
                }
            )

# def filter_data(request):
#     categories=request.GET.getlist('category[]')
#     brands=request.GET.getlist('brand[]')
#     minPrice=request.GET['minPrice']
#     maxPrice=request.GET['maxPrice']
#     allProducts=Product.objects.all().order_by('-id').distinct()
#     allProducts=allProducts.filter(productattribute__price__gte=minPrice)
#     allProducts=allProducts.filter(productattribute__price__lte=maxPrice)
#     if len(categories)>0:
#         allProducts=allProducts.filter(category__id__in=categories).distinct()
#     if len(brands)>0:
#         allProducts=allProducts.filter(brand__id__in=brands).distinct()
#     t=render_to_string('ajax/product-list.html',{'data':allProducts})
#     return JsonResponse({'data':t})

def filter_data(request):
    categories=request.GET.getlist('category[]')
    brands=request.GET.getlist('brand[]')
    minPrice=request.GET.get('minPrice', '')
    maxPrice=request.GET.get('maxPrice', '')
    allProducts=Product.objects.all().order_by('-id').distinct()
    if minPrice and minPrice.isdigit():
        allProducts=allProducts.filter(productattribute__price__gte=int(minPrice))
    if maxPrice and maxPrice.isdigit():
        allProducts=allProducts.filter(productattribute__price__lte=int(maxPrice))
    if len(categories)>0:
        allProducts=allProducts.filter(category__id__in=categories).distinct()
    if len(brands)>0:
        allProducts=allProducts.filter(brand__id__in=brands).distinct()
    t=render_to_string('ajax/product-list.html',{'data':allProducts})
    return JsonResponse({'data':t})

