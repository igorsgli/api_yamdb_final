from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Comment, Genre, Review, Title

import re

User = get_user_model()


class MixinUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=settings.LENGTH_USERNAME,
        required=True,
    )
    email = serializers.EmailField(
        max_length=settings.LENGTH_EMAIL,
        required=True,
    )
    first_name = serializers.CharField(
        max_length=settings.LENGTH_FIRST_NAME, required=False
    )
    last_name = serializers.CharField(
        max_length=settings.LENGTH_FIRST_NAME, required=False
    )
    confirmation_code = serializers.CharField(
        write_only=True, required=False
    )

    class Meta:
        model = User
        fields = '__all__'

    def validate_username(self, value):
        if re.fullmatch(settings.USERNAME_PATTERN, value) is None:
            raise serializers.ValidationError(
                'Имя пользователя не соответствует шаблону.'
            )
        if value == 'me':
            raise serializers.ValidationError(
                'Использовать имя <me> в качестве username запрещено.'
            )
        return value


class SignupSerializer(MixinUserSerializer):

    class Meta:
        model = User
        fields = ('email', 'username')


class TokenSerializer(MixinUserSerializer):
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class UserSerializer(MixinUserSerializer):
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'role',
            'first_name', 'last_name', 'bio',
        )


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug',)
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug',)
        model = Genre


class TitleSlugSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(many=True, slug_field='slug',
                                         queryset=Genre.objects.all())
    category = serializers.SlugRelatedField(slug_field='slug',
                                            queryset=Category.objects.all())

    class Meta:
        model = Title
        fields = '__all__'


class TitleGeneralSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.FloatField()

    class Meta:
        model = Title
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    title = serializers.PrimaryKeyRelatedField(
        read_only=True
    )
    score = serializers.IntegerField(min_value=1, max_value=10)

    class Meta:
        model = Review
        fields = '__all__'

    def create(self, validated_data):
        if Review.objects.filter(
            author=validated_data['author'], title=validated_data['title']
        ).exists():
            raise serializers.ValidationError(
                'Для одного произведения можно оставить только один отзыв!'
            )

        review = Review.objects.create(
            **validated_data,
        )

        return review


class CommetSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    review = serializers.PrimaryKeyRelatedField(
        read_only=True
    )

    class Meta:
        model = Comment
        fields = '__all__'
