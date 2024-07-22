from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Book, Review, UserProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = ['user', 'bio']

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        UserProfile.objects.create(user=user)
        return user

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'genre']

class BookDetailSerializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'genre', 'reviews']

    def get_reviews(self, obj):
        reviews = Review.objects.filter(book=obj)
        return ReviewSerializer(reviews, many=True).data

class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Review
        fields = ['id', 'book', 'user', 'rating']
