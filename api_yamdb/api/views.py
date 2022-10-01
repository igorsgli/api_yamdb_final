import random
import string

from django.core.mail import send_mail

from rest_framework import generics, status
from rest_framework.response import Response

from .serializers import SignupSerializer

from django.conf import settings
from django.contrib.auth import get_user_model


User = get_user_model()

def get_confirmation_code(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

class SignupView(generics.GenericAPIView):

    serializer_class = SignupSerializer

    def post(self, request):
        confirmation_code = get_confirmation_code(settings.CONFIRMATION_CODE_LENGTH)
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

        return Response(user_data, status=status.HTTP_201_CREATED)
