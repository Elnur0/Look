from django.contrib import admin
from modeltranslation.admin import TranslationAdmin


from .models import(
    Product, Category, Brends, 
    Size, Color, Company,
    Basket, ProductImage, ProductsReview
)





class ImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductAdmin(TranslationAdmin):
    inlines = (ImageInline,)


@admin.register(Product)
class ProductRegistr(ProductAdmin):
    list_display = ( 'title', 'category', 'price', 'sku', 'count', 'status', 'created_at', )
    list_filter = ('category', 'size', 'color')
    search_fields = ('title', )
    list_per_page = 10
    inlines = (ImageInline,)
    readonly_fields =( 'created_at', 'updated_at',)


class CategoryAdmin(TranslationAdmin):
    list_display =('name', 'parent', 'get_children_count')

    def get_children_count(self, obj):
            return obj.children.count()
    get_children_count.short_description = 'Children Count'

admin.site.register(Category, CategoryAdmin)



admin.site.register(Brends)
admin.site.register(Size)
admin.site.register(Color)
admin.site.register(Company)
admin.site.register(Basket)
admin.site.register(ProductsReview)



