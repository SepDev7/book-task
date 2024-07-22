from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    BookListView, BookDetailView,
    ReviewListView, ReviewDetailView,
    BookByGenreView, SuggestBooksView,
    UserProfileView, UserRegistrationView
)

urlpatterns = [
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', UserRegistrationView.as_view(), name='user_registration'),
    path('api/books/', BookListView.as_view(), name='book-list'),
    path('api/books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('api/reviews/', ReviewListView.as_view(), name='review-list'),
    path('api/reviews/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),
    path('api/books/genre/', BookByGenreView.as_view(), name='book-by-genre'),
    path('api/books/suggest/', SuggestBooksView.as_view(), name='suggest-books'),
    path('api/profile/', UserProfileView.as_view(), name='user-profile'),
]
