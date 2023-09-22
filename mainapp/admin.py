from django.contrib import admin

from .models import(
    Product, Category, Brends, 
    Size, Color, Company,
    Basket, ProductImage, ProductsReview
)


class ImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    inlines = (ImageInline,)





admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Brends)
admin.site.register(Size)
admin.site.register(Color)
admin.site.register(Company)
admin.site.register(Basket)
admin.site.register(ProductsReview)



