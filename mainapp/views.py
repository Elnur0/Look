from rest_framework import generics
from rest_framework.response import Response
from django.shortcuts import render
from django.db.models import Avg, F, FloatField
from django.db.models.functions import Coalesce

from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from services.permissions import CustomPermission

from .serializers import (
ProductSerializer, ProductDetailSerializer, 
CommentSerializer, WishlistSerializer,
BasketSerializer,
)
from .models import(
    Product, Category, Brends, 
    Size, Color, Company,
    Basket, ProductsReview,
)




class PrductListView(generics.ListAPIView):                         
    queryset = Product.objects.annotate(discount_price=Coalesce(
        F("discount"), 0, output_field=FloatField()),
        disc_price = F("price")*F("discount")/100,
        total_price=F("price")-F("disc_price")
        ).order_by("-created_at")
    serializer_class = ProductSerializer
    # permission_classes = (IsAuthenticated, )



class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.annotate(discount_price=Coalesce(
        F("discount"), 0, output_field=FloatField()),
        disc_price = F("price")*F("discount")/100,
        total_price=F("price")-F("disc_price")
        ).order_by("-created_at")

    serializer_class = ProductDetailSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        product = self.get_object()
        product.view +=1
        product.save()
        return super().get(request, *args, **kwargs)
    

    def put(self, request, *args, **kwargs):
        if request.method == "PUT":
            serializer = CommentSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user, product=self.get_object())
            return Response(serializer.data)
        return Response({})





class WishlistView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = WishlistSerializer
    lookup_field = "id"
    permission_classes = (IsAuthenticatedOrReadOnly,) 


    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,instance=self.get_object(), context={"user": request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
        


class BasketView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = BasketSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )


    def post(self, request, *args, **kwargs):
        data = {}
        product = Product.objects.get(id=kwargs.get("id"))
        create_basket = Basket.objects.get_or_create(user=request.user, products=product)
        data["success"] = create_basket[1]
        return Response(data)
    


class ReviewView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductsReview.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (CustomPermission, )
    lookup_field = "id"