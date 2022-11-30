# api/views.py
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from api.serializers import SignUpSerializer
from users.models import User


class SignUpSet(CreateAPIView):

    serializer_class = SignUpSerializer

    def post(self, request):
        user = request.data
        serializer = self.get_serializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        username = serializer.data['username']
        email = serializer.data['email']
        user = User.objects.get(username=username)

        confirmation_code = default_token_generator.make_token(user)

        send_mail(
            'Регистрация на YaMDb',
            f'Здравствуйте, {username}! Вы зарегистрировались на YaMDb.ru.'
            f'confirmation_code для получения токена:\n{confirmation_code}',
            'registrate@YaMDb.ru',
            (email,),
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
