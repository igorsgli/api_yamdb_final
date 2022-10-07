from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (filters, generics, mixins, permissions, status,
                            viewsets)
from rest_framework.decorators import action
from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api.filters import ModelFilter
from api.permissions import (AdminOnly, GeneralPermission,
                             IsAdminOrModeratorOrAuthorOrReadOnly)
from api.serializers import (CategorySerializer, CommetSerializer,
                             GenreSerializer, ReviewSerializer,
                             SignupSerializer, TitleGeneralSerializer,
                             TitleSlugSerializer, TokenSerializer,
                             UserSerializer)
from reviews.models import Category, Genre, Review, Title

from .utils import get_confirmation_code

User = get_user_model()


class AbstractsViewSet(mixins.CreateModelMixin,
                       mixins.ListModelMixin,
                       mixins.DestroyModelMixin,
                       viewsets.GenericViewSet,):
    pass


class SignupView(generics.GenericAPIView):

    serializer_class = SignupSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        confirmation_code = get_confirmation_code()
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
    pagination_class = PageNumberPagination
    permission_classes = (AdminOnly, )
    search_fields = ('username',)
    lookup_field = 'username'

    @action(detail=False, methods=['get', 'patch'],
            permission_classes=[permissions.IsAuthenticated])
    def me(self, request):

        if request.method == 'GET':
            serializer = self.get_serializer(self.request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        if request.method == 'PATCH':
            serializer = self.get_serializer(
                self.request.user,
                data=request.data,
                partial=True
            )
            if serializer.is_valid():
                serializer.save(role=self.request.user.role, partial=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(
                serializer.data,
                status=status.HTTP_400_BAD_REQUEST
            )


class CategoryViewSet(AbstractsViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [GeneralPermission]
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)


class GenreViewSet(AbstractsViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [GeneralPermission]
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    permission_classes = [GeneralPermission]
    filter_backends = [DjangoFilterBackend]
    filter_class = ModelFilter

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return TitleSlugSerializer
        return TitleGeneralSerializer

    def get_queryset(self):
        return Title.objects.all().annotate(rating=Avg('reviews__score'))


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAdminOrModeratorOrAuthorOrReadOnly
    ]
    pagination_class = LimitOffsetPagination

    def get_title(self):
        title_id = self.kwargs['title_id']
        return get_object_or_404(Title, id=title_id)

    def get_queryset(self):
        title = self.get_title()
        return title.reviews.all()

    def perform_create(self, serializer):
        title = self.get_title()
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommetSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAdminOrModeratorOrAuthorOrReadOnly
    ]
    pagination_class = LimitOffsetPagination

    def get_review(self):
        review_id = self.kwargs['review_id']
        return get_object_or_404(Review, id=review_id)

    def get_queryset(self):
        review = self.get_review()
        return review.comments.all()

    def perform_create(self, serializer):
        review = self.get_review()
        serializer.save(author=self.request.user, review=review)
