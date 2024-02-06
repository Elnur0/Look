from rest_framework import generics
from rest_framework.response import Response
from .models import (
Newsletter, FAQ, ContactUs, Settings, About, Shipping, Payment, Order, OrderItems
)
from .serializer import ( 
NewsletterSerializer, FAQSerializer,
ContactusSerializer, SettingsSerializer, AboutSerializer, 
ShippingSerializer, PaymentSerializer,
)
from services.permissions import HasAddDeletePermission
from mainapp.models import Basket



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



class AboutView(generics.ListAPIView):
    queryset = About.objects.all()
    serializer_class = AboutSerializer




class ShippingView(generics.CreateAPIView):
    queryset = Shipping.objects.all()
    serializer_class = ShippingSerializer

    def create(self, request, *args, **kwargs):
        queryset_ = Basket.objects.filter(user=request.user)
        
        shipping_method = request.data.get("shipping_method")
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(shippig_method=shipping_method)

        new_order = Order.objects.create(user=request.user)
        for basket in queryset_:
            new_items = OrderItems.objects.create(
                products=basket.products, quantity=basket.quantity
                )
            new_order.items.add(new_items)
        queryset_.delete()
        return Response(serializer.data)

    



class PaymentView(generics.CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

