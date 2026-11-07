from rest_framework import serializers

class ContactSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=15)
    subject = serializers.CharField(max_length=200)
    message = serializers.CharField()