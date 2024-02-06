from modeltranslation.translator import translator, TranslationOptions

from .models import Product, Category

class ProductTranslationOptions(TranslationOptions):
    fields = ("title", "description", "aditional_info",)

translator.register(Product, ProductTranslationOptions)


class CategoryTranslationOptions(TranslationOptions):
    fields = ("name", "parent",)

translator.register(Category, CategoryTranslationOptions)