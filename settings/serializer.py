from rest_framework import serializers

from .models import Newsletter, FAQ, ContactUs, Settings
from mainapp.serializers import CustomRichTextField


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