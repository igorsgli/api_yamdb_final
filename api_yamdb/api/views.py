import random
import string

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework import filters, permissions
from rest_framework.response import Response
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly
)
from rest_framework.pagination import PageNumberPagination
from rest_framework.pagination import LimitOffsetPagination
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Genre, Title, Review, Comment
from api.permissions import IsAdmin, IsAdminOrAuthorOrReadOnly, IsAuthorOrReadOnly
from api.serializers import (
    CategorySerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleSlugSerializer,
    TitleGeneralSerializer,
    CommetSerializer,
    SignupSerializer,
    TokenSerializer,
    UserSerializer,
)


User = get_user_model()


def get_confirmation_code(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


class SignupView(generics.GenericAPIView):

    serializer_class = SignupSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        confirmation_code = get_confirmation_code(
            settings.CONFIRMATION_CODE_LENGTH
        )
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(confirmation_code=confirmation_code)
        user_data = serializer.data
        user = User.objects.get(username=user_data['username'])
        send_mail(
            'subject: ',
            'confirmation code: ' + user.confirmation_code,
            'from.api.yamdb@example.com',
            [user_data['email']],
            fail_silently=False,
        )

        return Response(user_data, status=status.HTTP_200_OK)


class TokenView(generics.GenericAPIView):

    serializer_class = TokenSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(username=request.data['username'])
        token_value = RefreshToken.for_user(user).access_token
        serializer.save(token=token_value)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    pagination_class = PageNumberPagination
    permission_classes = [permissions.IsAdminUser]

    def get_object(self):
        if self.kwargs['username'] == 'me':
            return self.request.user
        return super().get_object()


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdmin]
    http_method_names = ['get', 'post']

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdmin]
    http_method_names = ['get', 'post']

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class TitleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrAuthorOrReadOnly]

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return TitleSlugSerializer
        return TitleGeneralSerializer

    def get_queryset(self):
        return Title.objects.all().annotate(rating=Avg('reviews__score'))


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = LimitOffsetPagination

    def get_title(self):
        title_id = self.kwargs['title_id']
        return get_object_or_404(Title, id=title_id)

    def perform_create(self, serializer):
        title = self.get_title()
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommetSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = LimitOffsetPagination

    def get_review(self):
        review_id = self.kwargs['review_id']
        return get_object_or_404(Review, id=review_id)

    def perform_create(self, serializer):
        review = self.get_review()
        serializer.save(author=self.request.user, review=review)