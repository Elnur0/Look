from rest_framework import serializers
import string
from django.db.models import Avg, F
from django.utils.html import strip_tags

from .models import (
    Product, ProductsReview, ProductImage,
    Basket, Category, Size, Color
    )

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ('id', 'name', 'code' )




class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ('id', 'name' )




class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'children')

    
    def to_representation(self, instance):
        repr_ = super().to_representation(instance)
        qs = Category.objects.filter(parent=instance)

        if  qs.exists():
            repr_['children'] = CategorySerializer(qs, many=True).data
        return repr_




class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ("image",)





class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    total_price = serializers.FloatField(read_only=True) 
    class Meta:
        model = Product
        fields = ('id', 'title', 'category', 'total_price', 'discount')


    def to_representation(self, instance):                
        repr_ = super().to_representation(instance)
        repr_["category"] = CategorySerializer(instance.category).data
        return repr_


    def to_representation(self, instance):
        repr_ = super().to_representation(instance)
        rating = instance.productsreview_set.aggregate(Avg(F("rating")))['rating__avg']

        rating_ = (rating or 0)

        image = instance.productimage_set.first()

        images = ProductImageSerializer(image).data

        repr_["image"] = images
        repr_["rating"] = round(rating_, 1)
        return repr_
        



class CustomRichTextField(serializers.Field):
    def to_representation(self, obj):
        return strip_tags(obj)




class ProductDetailSerializer(serializers.ModelSerializer):
    total_price = serializers.FloatField(read_only=True)
    description_ = CustomRichTextField(source="description", read_only=True) 
    class Meta:
        model = Product
        exclude = ("price", "description")
        extra_kwargs = {
            "title": {"read_only": True},
            "sku": {"read_only": True},
            "tags": {"read_only": True},
            "size": {"read_only": True},
            "color": {"read_only": True},
            "price": {"read_only": True},
            "discount": {"read_only": True},
            "category": {"read_only": True},
            "status": {"read_only": True},
            "wishlist": {"read_only": True},
            "count": {"read_only": True},
            "view": {"read_only": True},
        }

        
    def to_representation(self, instance):
        repr_ = super().to_representation(instance)
        rating = instance.productsreview_set.aggregate(Avg(F("rating")))['rating__avg']


        image = instance.productimage_set.first()

        images = ProductImageSerializer(image).data
        repr_["comments"] = CommentSerializer(instance.productsreview_set.all(), many=True).data
        repr_["image"] = images
        repr_["rating"] = round((rating or 0), 1)
        return repr_




class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductsReview
        fields = ("id", "message", "rating")
        extra_kwargs = {
            "id": {"read_only": True}
        }
    

    def to_representation(self, instance):
        repr_ = super().to_representation(instance)
        repr_["user"] = instance.user.email
        repr_["user_name"] = f"{instance.user.name} {instance.user.name}"
        return super().to_representation(instance)





class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("wishlist",)
        

    def update(self, instance, validated_data):
        user = self.context.get("user")
        if user in instance.wishlist.all():
            instance.wishlist.remove(user)
        else:
            instance.wishlist.add(user)
            instance.save()
        return instance
    


class BasketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Basket
        fields = ("products", )


class BasketListSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()
    quantity = serializers.SerializerMethodField()

    class Meta:
        model = Basket
        fields = ("products", "name", "image", "total_price", "quantity")
        extra_kwargs = {
            "products":{"read_only":True}
        }

    def get_name(self, obj):
        return obj.products.title
    
    def get_image(self, obj):
        return ProductImageSerializer(obj.products.productimage_set.first()).data
    
    def get_total_price(self, obj):
        disc_price = obj.products.price * (obj.products.discount or 0) / 100
        return obj.products.price - disc_price
    
    def get_quantity(self, obj):
        return obj.quantity

