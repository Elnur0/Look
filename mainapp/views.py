from rest_framework import generics
from rest_framework.response import Response
from django.shortcuts import render
from django.db.models import Avg, F, FloatField, Sum, ExpressionWrapper, Value
from django.db.models.functions import Coalesce

from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework import filters

from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from services.permissions import CustomPermission

from .serializers import (
ProductSerializer, ProductDetailSerializer, CommentSerializer,
WishlistSerializer, BasketSerializer, CategorySerializer, 
SizeSerializer, ColorSerializer, BasketListSerializer,
)

from .models import(
Product, Category, Brends, Size, Color,
Company, Basket, ProductsReview,
)

from .filters import ProductFilter
from settings.models import Order, OrderItems

from services.pagination import CustomPagination



class PrductListView(generics.ListAPIView):                         
    queryset = Product.objects.annotate(discount_price=Coalesce(
        F("discount"), 0, output_field=FloatField()),
        disc_price = F("price")*F("discount")/100,
        total_price=F("price")-F("disc_price")
        ).order_by("-created_at")
    serializer_class = ProductSerializer

    filterset_class = ProductFilter
    filter_backends = (DjangoFilterBackend,)
    pagination_class = (CustomPagination)

    # permission_classes = (IsAuthenticated, )

    # filter_backends = (filters.OrderingFilter,)
    # ordering_fields = ("total_price", "created_at", "category")

    # filterset_fields = ["category", "price"] 
    



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





class WishView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = WishlistSerializer
    lookup_field = "id"
    permission_classes = (IsAuthenticatedOrReadOnly,) 


    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,instance=self.get_object(), context={"user": request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
        


class WishlistView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = (CustomPagination)
    serializer_class =ProductSerializer

    def get_queryset(self):
        qs = Product.objects.filter(wishlist__in=[self.request.user])
        return qs



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


class BasketListView(generics.ListCreateAPIView):
    serializer_class = BasketListSerializer
    permission_classes = (IsAuthenticated, )
    pagination_class = (CustomPagination)


    def get_queryset(self):
        qs = Basket.objects.filter(user=self.request.user)
        return qs
    

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        
        subtotal_price_expr = Coalesce(Sum(ExpressionWrapper(F("products__price") * F("quantity"), output_field=FloatField()),output_field=FloatField()),Value(0,output_field=FloatField()))
        total_discount_expr = Coalesce(Sum(ExpressionWrapper((F("products__price") * F("products__discount" or 0) / 100) * F("quantity"), output_field=FloatField()), output_field=FloatField()), Value(0, output_field=FloatField()))
        total_price_expr = subtotal_price_expr - total_discount_expr

        subtotal_price = queryset.aggregate(subtotal_price=subtotal_price_expr)["subtotal_price"]
        total_discount_price = queryset.aggregate(total_discount=total_discount_expr)["total_discount"]
        total_price = queryset.aggregate(total_price=total_price_expr)["total_price"]
        serializer = BasketListSerializer(queryset, many=True)
        
        
        code = request.data.get("coupon")

        if code:
            if Company.objects.filter(coupon=code, status="Activate").exists():
                code_price = Company.objects.get(coupon=code).dis_price
                total_price = total_price - code_price
            else:
                return Response({"error": "Promokod aktiv deil."})
        else:
            code_price = None

        serializer = self.serializer_class(queryset, many=True).data

        cart_data = {
            "items": serializer,
            "subtotal_price": float(subtotal_price),
            "total_discount_price": float(total_discount_price),
            "total_price": float(total_price),
        }
        
        if code_price:
            cart_data.update({"coupon discount": code_price})

        return Response(cart_data, status=200)
    

    def post(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        if queryset:
            success = True
            order = Order.objects.create(user=request.user)
            for basket in queryset:
                items = OrderItems.objects.create(products=basket.products, quantity=basket.quantity)
                order.items.add(items)
        else:
            success = False
        return Response({"success":success})









class ReviewView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductsReview.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (CustomPermission, )
    lookup_field = "id"




class CategoryView(generics.ListAPIView):
    queryset = Category.objects.filter(parent__isnull=True)
    serializer_class = CategorySerializer




class SizeView(generics.ListAPIView):
    queryset = Size.objects.all()
    serializer_class = SizeSerializer



class ColorView(generics.ListAPIView):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer


