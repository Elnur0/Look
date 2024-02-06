from django.contrib import admin
from modeltranslation.admin import TranslationAdmin


from .models import Blogs, Category



@admin.register(Blogs)
class BlogAdmin(TranslationAdmin):
    list_display = ( 'title', 'category', 'is_published', 'created_at', 'image' )
    list_filter = ('category', 'is_published')
    search_fields = ('title', )
    list_editable = ('is_published',)
    list_per_page = 10

    fieldsets = ( ( 'Blog', {'fields': ('title', 'description', 'image', 'is_published', 'category')}), )


class CategoryAdmin(TranslationAdmin):
    list_display =('title',)

admin.site.register(Category, CategoryAdmin)
