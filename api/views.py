from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Book, Review, UserProfile
from .serializers import (
    BookSerializer, BookDetailSerializer,
    ReviewSerializer, UserProfileSerializer, UserRegistrationSerializer
)
from drf_yasg.utils import swagger_auto_schema

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Register a new user",
        responses={201: UserRegistrationSerializer}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class BookListView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve a list of all books",
        responses={200: BookSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new book",
        responses={201: BookSerializer}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookDetailSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve a specific book by ID",
        responses={200: BookDetailSerializer}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update a specific book by ID",
        responses={200: BookDetailSerializer}
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a specific book by ID",
        responses={204: 'No Content'}
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

class ReviewListView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve a list of all reviews",
        responses={200: ReviewSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new review",
        responses={201: ReviewSerializer}
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return super().post(request, *args, **kwargs)

class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve a specific review by ID",
        responses={200: ReviewSerializer}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update a specific review by ID",
        responses={200: ReviewSerializer}
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a specific review by ID",
        responses={204: 'No Content'}
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

class BookByGenreView(generics.ListAPIView):
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve a list of books by genre",
        responses={200: BookSerializer(many=True)}
    )
    def get_queryset(self):
        genre = self.request.query_params.get('genre', None)
        return Book.objects.filter(genre=genre)

class SuggestBooksView(generics.ListAPIView):
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Suggest books to the user based on past reviews",
        responses={200: BookSerializer(many=True)}
    )
    def get_queryset(self):
        user = self.request.user
        # Get genres of books reviewed by the user
        reviewed_genres = Review.objects.filter(user=user).values_list('book__genre', flat=True).distinct()
        # Suggest books that are in the same genres but not yet reviewed by the user
        suggested_books = Book.objects.filter(genre__in=reviewed_genres).exclude(reviews__user=user)
        return suggested_books

class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.userprofile

    @swagger_auto_schema(
        operation_description="Retrieve user profile",
        responses={200: UserProfileSerializer}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update user profile",
        responses={200: UserProfileSerializer}
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
