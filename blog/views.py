from rest_framework import generics

from .models import Blogs
from .serializer import BlogSerializer

from services.pagination import CustomPagination




class BlogView(generics.ListAPIView):
    queryset = Blogs.objects.filter(is_published=True).order_by("-created_at")
    serializer_class = BlogSerializer
    pagination_class = (CustomPagination)




class BlogDetailView(generics.RetrieveAPIView):
    queryset = Blogs.objects.filter(is_published=True).order_by("-created_at")
    serializer_class = BlogSerializer
    lookup_field = "id"