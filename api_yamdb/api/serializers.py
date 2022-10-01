from django.contrib.auth import get_user_model

from rest_framework import serializers


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