import django_filters

from .models import Product, Size, Category, Color, Brends
from blog.models import Blogs


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


# class AllSearch(django_filters.FilterSet):

#     def get_queryset(self):
#             search_query = self.request.query_params.get(self.search_param, '')

#             product_results = Product.objects.filter(title__icontains=search_query)
#             blog_results = Blogs.objects.filter(title__icontains=search_query)
#             brend_results = Brends.objects.filter(name__icontains=search_query)

#             all_results = list(product_results) + list(blog_results) + list(brend_results)

#             return all_results