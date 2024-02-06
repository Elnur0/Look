from modeltranslation.translator import translator, TranslationOptions

from .models import Blogs, Category


class BlogTranslationOptions(TranslationOptions):
    fields = ("title", "description",)

translator.register(Blogs, BlogTranslationOptions)



class CategoryTranslationOptions(TranslationOptions):
    fields = ("title",)

translator.register(Category, CategoryTranslationOptions)
