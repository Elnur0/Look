from rest_framework import serializers
from mainapp.serializers import CustomRichTextField

from .models import (
Newsletter, FAQ, ContactUs, Settings, 
About, Shipping, Payment, Country,
)



class NewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newsletter
        fields = ('email',)




class FAQSerializer(serializers.ModelSerializer):
    question_ = CustomRichTextField(source='question')
    answer_ = CustomRichTextField(source='answer')
    class Meta:
        model = FAQ
        fields = ('question_','answer_')




class ContactusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        exclude = ("id", "created_at", "updated_at")




class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settings
        exclude = ("id",)



class AboutSerializer(serializers.ModelSerializer):
    description_ = CustomRichTextField(source='description')
    class Meta:
        model = About
        fields = ("title", "description_", "image")


class ShippingSerializer(serializers.ModelSerializer):
    ...