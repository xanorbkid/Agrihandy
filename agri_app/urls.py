from django.urls import path
from .views import *

urlpatterns = [
    path('', home,name='home'),
    path('search', search,name='search'),
    path('brand_list', brand_list , name='brand_list'),
    path('category-product-list/<int:cat_id>',category_product_list, name='category-product-list'),
    path('brand-product-list/<int:brand_id>', brand_product_list, name='brand-product-list'),
    path('category/', category_list, name='category'),
    path('shop/', shop,name='shop'),
    path('product/<str:slug>/<int:id>', product_detail, name='product_detail'),
    # path('product/', product_details,name='products'),
    path('about/', about,name='about'),
    path('contact/', contact,name='contact'),
    path('blog/', blog, name='blog'),
    path('filter-data', filter_data, name='filter_data'),
    
]