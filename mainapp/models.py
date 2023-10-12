from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model, authenticate
from taggit.managers import TaggableManager

from .generator import generate_random_number


User = get_user_model()




Status = (
    ('In stock', 'In stock'),
    ('Sold', 'Sold'),
    ('will available','will available'),
    ('New', 'New')
)


COMPANY_STATUS_CHOICES = (
    ("Activate", "Activate"),
    ("Deactivate", "Deactivate"),

)


Rating = (
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
)



class DateMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        abstract = True





class BaseModel(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)


    class Meta:
        abstract = True





class Size(BaseModel,DateMixin):
    length = models.CharField(max_length=100, blank=True, null=True)
    hip = models.CharField(max_length=100, blank=True, null=True)
    weight = models.CharField(max_length=100, blank=True, null=True) 


    def __str__(self):
        return self.name
    

    class Meta:
        verbose_name = 'Size'
        verbose_name_plural = 'Sizes'





class Color(BaseModel,DateMixin):
    code = models.CharField(max_length=100, blank=True, null=True)


    def __str__(self):
        return self.name
    

    class Meta:
        verbose_name = 'Color'
        verbose_name_plural = 'Colors'
    




class Category(BaseModel,MPTTModel,DateMixin):
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')


    def __str__(self):
        return self.name
    

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'




    
def upload_to_brends(instance, filename):
    return f"brends/{instance.brends.name}/{filename}"



class Brends(BaseModel,DateMixin):
    description = RichTextField(blank=True, null=True)
    icone = models.ImageField(upload_to=upload_to_brends)


    def __str__(self):
        return self.name
    

    class Meta:
        verbose_name = 'Brend'
        verbose_name_plural = 'Brends'








class Company(DateMixin):
    dis_price = models.FloatField(blank=True, null=True)
    coupon = models.CharField(max_length=100,blank=True, null=True, unique=True)
    status = models.CharField(max_length=50, choices=COMPANY_STATUS_CHOICES, default="Activate")


    def __str__(self) -> str:
        return self.coupon

    




class Product(DateMixin):
    title = models.CharField(max_length=100, blank=True, null=True)
    description = RichTextField(blank=True, null=True)
    size = models.ManyToManyField(Size, blank=True)
    color = models.ManyToManyField(Color, blank=True)
    view = models.IntegerField(default=0)
    price = models.FloatField(blank=True, null=True)
    discount = models.FloatField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(max_length=100, choices = Status, blank=True, null=True)
    wishlist = models.ManyToManyField(User, blank=True) 
    tags = TaggableManager()
    sku = models.CharField(max_length=6, default=generate_random_number, unique=True, blank=True, null=True)
    count = models.PositiveIntegerField(default=0)


    def save(self, *args, **kwargs):
        if not self.sku:
            self.sku = generate_random_number()
        super().save(*args, **kwargs)


    def __str__(self):
        return self.title
    

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'





def upload_to_product(instance, filename):
    return f"product/{instance.product.title}/{filename}"






class Basket(DateMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    products = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
            return self.user.email
    

    class Meta:
        verbose_name = 'Basket'
        verbose_name_plural = 'Basket'



class ProductImage(DateMixin):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_to_product, blank=True, null=True)


    def __str__(self):
        return self.product.title
    

    class Meta:
        verbose_name = 'ProductImage'
        verbose_name_plural = 'ProductImages'

    



class ProductsReview(MPTTModel, DateMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey("mainapp.Product", on_delete=models.CASCADE, blank=True, null=True)
    parent = TreeForeignKey("self",on_delete=models.CASCADE, related_name="children", blank=True, null=True)
    message = models.TextField(max_length=300)
    rating = models.PositiveIntegerField(blank=True, null=True, choices=Rating)


    def __str__(self):
        return self.user.email
    

    class Meta:
        verbose_name_plural = "Comments"
        verbose_name = "Comment"