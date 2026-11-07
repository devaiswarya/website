from rest_framework import serializers
from django.core.validators import URLValidator

HTTP_URL_VALIDATOR = URLValidator(
    schemes=["http", "https"]
)


class ProductSerializer(serializers.Serializer):
    product_name = serializers.CharField(
        required=True
    )
    product_id = serializers.CharField(
    required=True,  max_length=200
)
    category_id = serializers.CharField(
        required=True
    )

    primary_category_id = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True
    )

    secondary_category_id = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True
    )

    unit_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=True
    )

    initial_stock_level = serializers.IntegerField(
        required=True,
        min_value=0
    )

    short_description = serializers.CharField(
        required=True
    )

    image_1 = serializers.URLField(
        required=True,
        validators=[HTTP_URL_VALIDATOR]
    )

    image_2 = serializers.URLField(
        required=False,
        allow_null=True,
        validators=[HTTP_URL_VALIDATOR]
    )

    image_3 = serializers.URLField(
        required=False,
        allow_null=True,
        validators=[HTTP_URL_VALIDATOR]
    )

    image_4 = serializers.URLField(
            required=False,
            allow_null=True,
            validators=[HTTP_URL_VALIDATOR]
        )

    variants = serializers.JSONField(
        required=False
    )

    status = serializers.ChoiceField(
        choices=["Active", "Inactive"],
        required=False,
        default="Active"
    )

    is_deleted = serializers.BooleanField(
        required=False,
        default=False
    )


class ProductImageUpdateSerializer(serializers.Serializer):

    image_1 = serializers.URLField(
        required=False,
        allow_null=True,
        validators=[HTTP_URL_VALIDATOR]
    )

    image_2 = serializers.URLField(
        required=False,
        allow_null=True,
        validators=[HTTP_URL_VALIDATOR]
    )

    image_3 = serializers.URLField(
        required=False,
        allow_null=True,
        validators=[HTTP_URL_VALIDATOR]
    )

    image_4 = serializers.URLField(
            required=False,
            allow_null=True,
            validators=[HTTP_URL_VALIDATOR]
        )