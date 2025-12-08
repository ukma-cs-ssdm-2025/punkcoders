from rest_framework import serializers
from restaurant.models import Category, Dish


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the Category model.
    """

    class Meta:
        model = Category
        fields = ["id", "name", "slug"]
        read_only_fields = ["slug"]


class DishSerializer(serializers.ModelSerializer):
    """
    The main serializer for the Dish model. Handles reading, writing, and file uploads.
    """

    # --- For Reading ---
    category = CategorySerializer(read_only=True)

    # --- For Writing ---
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source="category", write_only=True
    )

    # This field handles the actual image file upload.
    photo = serializers.ImageField(required=False, allow_null=True, write_only=True)
    # and this the image download
    photo_url = serializers.SerializerMethodField()

    is_available = serializers.BooleanField(default=True, required=False)

    class Meta:
        model = Dish
        fields = [
            "id",
            "name",
            "description",
            "price",
            "photo",
            "photo_url",
            "is_available",
            "category",
            "category_id",
        ]

    def get_photo_url(self, obj):
        """
        Returns the absolute URL for the dish photo, or None if no photo exists.
        """
        if not obj.photo:
            return None
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(obj.photo.url)
        return obj.photo.url
