from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title, UserToken

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
        email = data.get('email')
        username = data.get('username')

        if username == 'me':
            raise serializers.ValidationError(
                'Использовать имя <me> в качестве username запрещено.'
            )

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'User с таким email уже существует.'
            )

        return data


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True, required=True)
    confirmation_code = serializers.CharField(
        write_only=True,
        required=True,
    )
    token = serializers.CharField(required=False)

    class Meta:
        model = UserToken
        fields = ('token', 'username', 'confirmation_code')

    def validate(self, data):
        username = data.get('username')
        confirmation_code = data.get('confirmation_code')

        if username is None:
            raise serializers.ValidationError(
                'Требуется ввести username.'
            )

        if confirmation_code is None:
            raise serializers.ValidationError(
                'Требуется ввести confirmation_code.'
            )

        user = get_object_or_404(User, username=username)

        if user.confirmation_code != confirmation_code:
            raise serializers.ValidationError(
                'Неправильный confirmation code.'
            )

        return data


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=None, min_length=None, allow_blank=False, required=True
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'role',
            'first_name', 'last_name', 'bio',
        )

    def validate(self, data):
        email = data.get('email', '')

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'User с таким email уже существует.'
            )

        return data


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
