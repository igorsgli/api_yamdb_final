from django.shortcuts import get_object_or_404
from django.db.models import Avg
from rest_framework.response import Response
from rest_framework import status

from rest_framework import viewsets
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly
)
from rest_framework.pagination import LimitOffsetPagination

from reviews.models import Category, Genre, Title, Review, Comment
from api.permissions import IsAdmin, IsAdminOrAuthorOrReadOnly, IsAuthorOrReadOnly

from api.serializers import (
    CategorySerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleSlugSerializer,
    TitleGeneralSerializer,
    CommetSerializer
)


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
