from rest_framework import serializers
from .models import *

#serializes the Book model
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['title','publication_year','author']

        # check the publication year is not in the future
        def validate(self,data):
            if data['publiation_year'] > 2024:
                raise serializers.ValidationError("Book has not published yet.")

class AuthorSerializer(serializers.ModelSerializer):
    #nested serializer
    books = BookSerializer(many=True, read_only=True)
    class Meta:
        model =  Author
        fields = ['name','books']