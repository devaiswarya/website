from rest_framework import serializers


# Add to Cart Request Serializer
class AddToCartSerializer(serializers.Serializer):

    product_id = serializers.CharField(
        required=True,
        max_length=200
    )

    quantity = serializers.IntegerField(
        required=False,
        default=1,
        min_value=1
    )

    variant_name = serializers.CharField(
        required=False,
        allow_null=True,
        allow_blank=True
    )


# Cart Item Response Serializer
class CartItemSerializer(serializers.Serializer):

    product_id = serializers.CharField()

    product_name = serializers.CharField(
        allow_null=True
    )

    product_type = serializers.CharField(
        allow_null=True
    )

    category_name = serializers.CharField(
        allow_null=True
    )

    variant_name = serializers.CharField(
        allow_null=True
    )

    unit_price = serializers.FloatField()

    quantity = serializers.IntegerField()

    subtotal = serializers.FloatField()

    image = serializers.URLField(
        allow_null=True
    )


# Get Cart Response Serializer
class GetCartSerializer(serializers.Serializer):

    status = serializers.BooleanField()

    message = serializers.CharField()

    total_items = serializers.IntegerField()

    total_amount = serializers.FloatField()

    cart = CartItemSerializer(many=True)