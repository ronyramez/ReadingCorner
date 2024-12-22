from rest_framework import serializers

class BookSerializer(serializers.Serializer):
    Author = serializers.CharField(max_length=255)
    Language = serializers.CharField(max_length=100)
    ISBN = serializers.CharField(max_length=20)
    description = serializers.CharField(max_length=1000)
    BookName = serializers.CharField(max_length=255)
    BookId = serializers.IntegerField()
    category = serializers.CharField(max_length=100)
    Publisher = serializers.CharField(max_length=255)
    PublishingNumber = serializers.CharField(max_length=100)
    PublishingYear = serializers.IntegerField()
