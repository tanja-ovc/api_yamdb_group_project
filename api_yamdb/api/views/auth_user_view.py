import random
import string

from django.core.mail import send_mail
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from users.models import MyUser
from api.serializers import (SendConfirmationCodeSerializer,
                             CompareConfirmationCodesSerializer,
                             MyUserSerializer)


def generate_confirmation_code():
    chars = string.digits + string.ascii_letters
    return ''.join(random.sample(chars, 20))


@api_view(['POST'])
def send_confirmation_code(request):
    serializer = SendConfirmationCodeSerializer(data=request.data)
    email = request.data.get('email')
    username = request.data.get('username')

    if serializer.is_valid():
        confirmation_code = generate_confirmation_code()
        MyUser.objects.update_or_create(
            defaults={
                'confirmation_code': confirmation_code
            },
            email=email,
            username=username,
        )
        subject = 'Ваш код подтверждения на YaMDb'
        message = f'Код подтверждения {confirmation_code}'
        send_mail(subject, message, 'support@yamdb.ru', [email])
        return Response(f'Код подтверждения отправлен на адрес {email}', status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyUserViewSet(viewsets.ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer
