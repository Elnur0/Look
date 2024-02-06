from modeltranslation.translator import translator, TranslationOptions

from .models import FAQ, About

class FaqTranslationsOptions(TranslationOptions):
    fields = ('question','answer')

translator.register(FAQ, FaqTranslationsOptions)



class AboutTranslationsOptions(TranslationOptions):
    fields = ('title', 'description',)

translator.register(About, AboutTranslationsOptions)