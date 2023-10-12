import django_filters

from .models import Product, Size, Category, Color


class ProductFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr="icontains")
    price_max = django_filters.NumberFilter(field_name="total_price", lookup_expr="gte")
    price_min = django_filters.NumberFilter(field_name="total_price", lookup_expr="lte")
    category = django_filters.ModelChoiceFilter(field_name="category", queryset=Category.objects.all())
    size = django_filters.ModelChoiceFilter(field_name="size", queryset=Size.objects.all())
    color = django_filters.ModelChoiceFilter(field_name="color", queryset=Color.objects.all())

    class Meta:
        model = Product
        fields = ("title", "price_max", "price_min", "category", "size", "color")