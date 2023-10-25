from django.db import models
from ckeditor.fields import RichTextField



class DateMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        abstract = True




class Category(DateMixin):
    title = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'





def upload_to_blog(instance, filename):
    return f"blogs/{instance.title}/{filename}"


class Blogs(DateMixin):
    title = models.CharField(max_length=100)
    description = RichTextField()
    image = models.ImageField(upload_to=upload_to_blog)
    is_published = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name="category", blank=True, null=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Blog'
        verbose_name_plural = 'Blogs'