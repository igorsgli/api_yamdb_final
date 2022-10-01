from dataclasses import fields
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()

class SignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=None, min_length=None, allow_blank=False, required=True
    )
    confirmation_code = serializers.CharField(
        write_only=True, required=False
    )

    class Meta:
        model = User
        fields = ('email', 'username', 'confirmation_code')

    def validate(self, data):
        email = data.get('email', '')
        username = data.get('username', '')

        if not username.isalnum():
            raise serializers.ValidationError(
                'Username должен состоять из буквенно-цифровых символов.'
            )
        
        if username == 'me':
            raise serializers.ValidationError(
                 'Использовать имя <me> в качестве username запрещено.'
            )

        if User.objects.filter(email=email).count() > 0:
            raise serializers.ValidationError(
                'User с таким email уже существует.'
            )

        return data

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

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

    class Meta:
        model = Review
        fields = '__all__'


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