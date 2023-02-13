from django.contrib import admin
from .models import *

# Register your models here.

class BrandAdmin(admin.ModelAdmin):
    list_display=('title','description','image_tag', 'address', 'mobile')

admin.site.register(Brand, BrandAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display=('id','title','category','brand','status','is_featured','barcode','image','image_two')
    list_editable=('status','is_featured')
admin.site.register(Product,ProductAdmin)


admin.site.register(Banner)

class CategoryAdmin(admin.ModelAdmin):
    list_display=('title','image_tag')

admin.site.register(Category,CategoryAdmin)

class ProductAttributeAdmin(admin.ModelAdmin):
    list_display=('product','quantity','price','image_three','upload_date')

admin.site.register(ProductAttribute,ProductAttributeAdmin)
admin.site.register(CartOrder)
admin.site.register(CartOrderItems)
# admin.site.register(Product)