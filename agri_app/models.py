from django.db import models
from django.contrib.auth.models import User
from django.utils.html import mark_safe
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from django.core.files import File

# Create your models here.

# CATEGORY_CHOICES = (
#     ('Vegetables', 'Vegetables'),
#     ('Fruits', 'Fruits'),
#     ('Tuber Crops', 'Tuber Crops'),
#     ('Poultry', 'Poultry'),
#     ('Fishery', 'Fishery'),
#     ('Livestock', 'Livestock'),
# )

LABEL_CHOICES = (
    ('New', 'New'),
    ('Sale', 'Sale'),
    ('Out-stock', 'Out-stock'),
)
#Banner
class Banner(models.Model):
    img=models.ImageField(default='banner.jpg', upload_to='static/images')
    alt_text= models.CharField(max_length=300)

    class Meta:
        verbose_name_plural='1. Banners'

    def __str__(self):
        return self.alt_text

#Vendors/Brand
class Brand(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(default='default.jpg', upload_to='static/images')
    description =models.TextField(blank=True, null=True)
    address=models.CharField(max_length=200, null=True, blank=True)
    mobile =models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name_plural='2. Brands'

    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))    

    def __str__(self):
            return self.title 

#Categories
class Category(models.Model):
    title=models.CharField(max_length=100)
    image = models.ImageField(default='default.jpg', upload_to='static/images')
    
    class Meta:
        verbose_name_plural='3. Categories'
    
    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    
    def __str__(self):
        return self.title
    
#Product
class Product(models.Model):
    title = models.CharField(max_length=200)
    brand=models.ForeignKey(Brand,on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='static/images', blank=True, null=True)
    image_two = models.ImageField(default='default.jpg', upload_to='static/images', blank=True, null=True)
    discount_price = models.IntegerField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True, max_length=100)
    description = models.TextField()
    overview = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    label = models.CharField(choices= LABEL_CHOICES, max_length=20)
    status = models.CharField(max_length=200)
    is_featured=models.BooleanField(default=False)
    barcode = models.ImageField(upload_to='static/images/barcodes/', blank=True, null=True)

    class Meta:
        verbose_name_plural='4. Products'

    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))        

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):          # overriding save() 
        COD128 = barcode.get_barcode_class('code128')
        rv = BytesIO()
        code = COD128(f'{self.title}', writer=ImageWriter()).write(rv)
        self.barcode.save(f'{self.title}.png', File(rv), save=False)
        return super().save(*args, **kwargs)
    
#Product Attribute    
class ProductAttribute(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=0, blank=True, null=True)
    price=models.IntegerField(default=0)
    image_three = models.ImageField(default='default.jpg', upload_to='static/images', blank=True, null=True)
    image_four = models.ImageField(default='default.jpg', upload_to='static/images', blank=True, null=True)
    image_five = models.ImageField(default='default.jpg', upload_to='static/images', blank=True, null=True)
    upload_date= models.DateTimeField(auto_now=True, blank=True, null=True)

    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image_three.url))        
    
    class Meta:
        verbose_name_plural='5. Product Attributes'

    def __str__(self):
            return self.product.title
    
#Order
status_choice=(
     ('process','In Process'),
     ('shipped','Shipped'),
     ('delivered','Delivered'),
) 

class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    total_amt=models.FloatField()
    paid_status = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)
    order_status=models.CharField(choices=status_choice, max_length=100)
    order_date =models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural='6. Orders'

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

#Order Items
class CartOrderItems(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order=models.ForeignKey(CartOrder,on_delete=models.CASCADE)
    invoice_no=models.CharField(max_length=150)
    item=models.CharField(max_length=150)
    image=models.CharField(max_length=200)
    qty=models.IntegerField()
    price=models.FloatField()
    total=models.FloatField()

    class Meta:
        verbose_name_plural='7. Ordered_items'

    def __str__(self):
         return self.user.username

# class CartOrderItem(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     ordered = models.BooleanField(default=False)
#     start_date = models.DateTimeField(auto_now=True)
#     ordered_date= models.DateTimeField()

#     def __str__(self):
#         return self.user.username