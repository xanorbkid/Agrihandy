from .models import Product,ProductAttribute
from django.db.models import Min,Max
from django.core.paginator import Paginator



def get_filters(request):
    cats=Product.objects.distinct().values('category__title','category__id')
    brands=Product.objects.distinct().values('brand__title','brand__id')
    # colors=ProductAttribute.objects.distinct().values('color__title','color__id','color__color_code')
    # sizes=ProductAttribute.objects.distinct().values('size__title','size__id')
    minMaxPrice=ProductAttribute.objects.aggregate(Min('price'),Max('price'))
    object_list =Product.objects.all()

    paginator = Paginator(object_list, 2) # Show 2 objects per page

    page = request.GET.get('page')
    objects = paginator.get_page(page)
    data={
        'cats':cats,
        'brands':brands,
        # 'colors':colors,
        # 'sizes':sizes,
        'minMaxPrice':minMaxPrice,
        'objects':objects
    }
    
    return data
