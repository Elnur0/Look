from django.db import models
from ckeditor.fields import RichTextField
from mainapp.models import Product
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.

class DateMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        

def upload_to_logo(instance, filename):
    return f"logo/{instance.logo}/{filename}"

class Settings(DateMixin):
    logo = models.ImageField(upload_to=upload_to_logo, blank=True, null=True)
    address = RichTextField(blank=True, null=True)
    number = models.CharField( max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    

    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = 'Setting'
        verbose_name_plural = 'Setting'




class Branch(DateMixin):
    country = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    work_hour = models.CharField(max_length=150)

    def __str__(self):
        return self.country
    
    class Meta:
        verbose_name = 'Branch'
        verbose_name_plural = 'Branchs'


         

class FAQ(DateMixin):
    question = RichTextField(max_length=300, verbose_name=("Sual"))
    answer = RichTextField(max_length=10000, verbose_name=("Cavab"))
    order = models.IntegerField(default=0, verbose_name=("Sıra"))

    def __str__(self):
        return "{}".format(self.question)

    class Meta:
        ordering = ("order",)



class OrderItems(DateMixin):
    products = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.products.title
    

    
class Order(DateMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItems, blank=True)

    def __str__(self):
        return self.user.email
    
    class Meta:
        verbose_name_plural = "Orders"
        verbose_name = "Order"
        
        


class Newsletter(DateMixin):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name_plural = "Newsletters"
        verbose_name = "Newsletter"




class ContactUs(DateMixin):
    firs_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.EmailField()
    messages = models.TextField()

    def __str__(self):
        return f"{self.firs_name} {self.last_name}"
    
    class Meta:
        verbose_name_plural = "Contacts"
        verbose_name = "ContactUs"




class About(DateMixin):


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        About.objects.exclude(id=self.id).delete()