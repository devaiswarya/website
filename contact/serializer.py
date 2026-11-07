# from rest_framework import serializers

# class ContactSerializer(serializers.Serializer):
#     name = serializers.CharField(max_length=100)
#     email = serializers.EmailField()
#     phone = serializers.CharField(max_length=15)
#     subject = serializers.CharField(max_length=200)
#     message = serializers.CharField()

from rest_framework import serializers

from .db import contacts_collection


class ContactSerializer(serializers.Serializer):

    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=15)
    message = serializers.CharField()

    def create(self, validated_data):

        result = contacts_collection.insert_one(validated_data)

        validated_data["_id"] = str(result.inserted_id)

        return validated_data