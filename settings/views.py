from rest_framework import generics

from .models import Newsletter, FAQ, ContactUs, Settings
from .serializer import NewsletterSerializer, FAQSerializer, ContactusSerializer, SettingsSerializer
from services.permissions import HasAddDeletePermission



class NewslettercreateView(generics.CreateAPIView):
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer



class FAQListView(generics.ListAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer



class ContactView(generics.CreateAPIView):
    queryset = ContactUs.objects.all()
    serializer_class = ContactusSerializer




class SettingsView(generics.ListAPIView):
    queryset = Settings.objects.all()
    serializer_class = SettingsSerializer
    # permission_classes = (HasAddDeletePermission, )
