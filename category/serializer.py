from rest_framework import serializers
from django.core.validators import URLValidator

HTTP_URL_VALIDATOR = URLValidator(schemes=["http", "https"])

class CategorySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    parent_id = serializers.CharField(
        required=False,
        allow_null=True,
        allow_blank=True
    )
    image = serializers.URLField(
        required=False,
        allow_null=True,
        validators=[HTTP_URL_VALIDATOR]
    )
    description = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True
    )
    status = serializers.ChoiceField(
        choices=["Active", "Inactive"],
        required=False,
        default="Active"
    )