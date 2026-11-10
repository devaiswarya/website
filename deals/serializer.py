from rest_framework import serializers

class DealSerializer(serializers.Serializer):

    product_id = serializers.CharField(
        required=True
    )

    offer_price = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        required=True
    )

    offer_title = serializers.CharField(
        required=False,
        default="Deal of the Day"
    )

    start_date = serializers.DateField(
        required=True,
        input_formats=["%Y-%m-%d"]
    )

    end_date = serializers.DateField(
        required=True,
        input_formats=["%Y-%m-%d"]
    )

    status = serializers.BooleanField(
        required=False,
        default=True
    )

    def validate_offer_price(self, value):

        if value <= 0:
            raise serializers.ValidationError(
                "Offer price must be greater than zero"
            )

        return value

    def validate(self, data):

        start_date = data.get("start_date")
        end_date = data.get("end_date")

        if start_date and end_date:

            if start_date > end_date:
                raise serializers.ValidationError({
                    "end_date":
                    "End date must be after start date"
                })

        return data