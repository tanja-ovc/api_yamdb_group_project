import random
import string

from api.permissions import AdminPermissions
from api.serializers import (CompareConfirmationCodesSerializer,
                             MyUserSerializer, SendConfirmationCodeSerializer)
from django.contrib.auth.hashers import check_password, make_password
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from users.models import MyUser


def generate_confirmation_code():
    chars = string.digits + string.ascii_letters
    return ''.join(random.sample(chars, 20))


@api_view(['POST'])
def send_confirmation_code(request):
    serializer = SendConfirmationCodeSerializer(data=request.data)
    email = request.data.get('email')
    username = request.data.get('username')
    if username == 'me':
        return Response(
            'Пользователя с таким именем создать нельзя',
            status=status.HTTP_400_BAD_REQUEST
        )
    if (
            MyUser.objects.filter(email=email).exists()
            or MyUser.objects.filter(username=username).exists()
    ):
        return Response(
            'Такой email уже зарегистрирован',
            status=status.HTTP_400_BAD_REQUEST
        )

    if serializer.is_valid():
        confirmation_code = generate_confirmation_code()
        MyUser.objects.update_or_create(
            defaults={
                'confirmation_code': make_password(
                    confirmation_code,
                    salt=None,
                    hasher='argon2'
                )
            },
            email=email,
            username=username,
        )
        subject = 'Your confirmation code for YaMDb'
        message = f'Код подтверждения {confirmation_code}'
        send_mail(subject, message, 'support@yamdb.ru', [email])
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def compare_confirmation_code(request):
    serializer = CompareConfirmationCodesSerializer(data=request.data)
    if serializer.is_valid():
        username = request.data.get('username')
        confirmation_code = request.data.get('confirmation_code')
        user = get_object_or_404(MyUser, username=username)
        if check_password(confirmation_code, user.confirmation_code):
            return Response({'token': f'{AccessToken.for_user(user)}'})
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyUserViewSet(viewsets.ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer
    permission_classes = (AdminPermissions,)
    lookup_field = 'username'


class UserAPI(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            user = get_object_or_404(MyUser, username=request.user.username)
            serializer = MyUserSerializer(user)
            return Response(serializer.data)
        return Response(
            'Для просмотра нужно авторизоваться',
            status=status.HTTP_401_UNAUTHORIZED
        )

    def patch(self, request):
        if request.user.is_authenticated:
            user = get_object_or_404(MyUser, username=request.user.username)
            serializer = MyUserSerializer(
                user,
                data=request.data,
                partial=True
            )
            if serializer.is_valid():
                serializer.validated_data.pop('role', None)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            'Для изменения необходимо авторизоваться',
            status=status.HTTP_401_UNAUTHORIZED
        )
