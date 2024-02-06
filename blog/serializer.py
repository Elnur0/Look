from rest_framework import serializers

from .models import Blogs


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blogs
        exclude = ("updated_at", "title_az", "title_en", "description_az", "description_en", "is_published")
