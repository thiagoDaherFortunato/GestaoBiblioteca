from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer, ValidationError, EmailField, CharField, Serializer

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()


class CadastroUsuarioSerializer(ModelSerializer):
    email = EmailField(label='email')
    email_confirma = EmailField(label='confirme email')

    class Meta:
        model = User
        fields = ['first_name',
                  'last_name',
                  'username',
                  'email',
                  'email_confirma',
                  'password'
                  ]

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        senha = validated_data['password']
        email_confirma = validated_data['email_confirma']

        if User.objects.filter(username=username).exists():
            raise ValidationError("Informar outro username")

        if User.objects.filter(email=email).exists():
            raise ValidationError("Email já associado a um usuário cadastrado")

        if email != email_confirma:
            raise ValidationError("Os emails digitados são diferentes")
        usuario_novo = User(
            username=username,
            email=email
        )
        usuario_novo.set_password(senha)
        usuario_novo.first_name = validated_data['first_name']
        usuario_novo.last_name = validated_data['last_name']
        usuario_novo.save()
        return validated_data



class UserListarSerializer(ModelSerializer):

    email = EmailField(label='email')

    class Meta:
        ordering = ['-id']
        model = User
        fields = ['id',
                  'first_name',
                  'last_name',
                  'username',
                  'email'
                  ]


class LoginSerializer(ModelSerializer):

    token = CharField(allow_blank=True, read_only=True)
    username = CharField(allow_blank=True, required=True)
    email = CharField(label='Email Address', allow_blank=True, required=False)

    class Meta:
        model = User
        fields = ['id',
                  'username',
                  'email',
                  'token',
                  'password'
                  ]
        extra_kwards = {'password': {'write_only': True}}

    def validate(self, validated_data):

        username = validated_data.get("username", None)
        senha = validated_data.get("password")

        if not username:
            raise ValidationError("Informe o login para acessar")

        usuario = User.objects.filter(username=username)

        if usuario.exists() and usuario.count() == 1:
            usuario = usuario.first()
        else:
            raise ValidationError("Username incorreto")

        if usuario:
            if not usuario.check_password(senha):
                raise ValidationError("Senha incorreta")

        token, created = Token.objects.get_or_create(user=usuario)

        if not created:
            token.save()
        validated_data["id"] = usuario.id
        validated_data["username"] = usuario.username
        validated_data["token"] = token.key
        validated_data["password"] = ''

        return validated_data

class LogoutSerializer(ModelSerializer):
        token = CharField(allow_blank=True, read_only=True)
        username = CharField(allow_blank=True, required=False)
        email = EmailField(label='Email Address', allow_blank=True, required=True)

        class Meta:
            model = User
            fields = ['username',
                      'email',
                      'password',
                      'token'
                      ]

        def sair(self, request):
            try:
                username = request.get("username")
                user = User.objects.filter(Q(username=username)).distinct()

                if user.exists() and user.count() == 1:
                    user_obj = user.first()
                else:
                    raise ValidationError("Usuario incorreto")
                token, created = Token.objects.get_or_create(user=user_obj)

                if not created:
                    token.delete()
                else:
                    raise ValidationError("Token incorreto")

            except (AttributeError, ObjectDoesNotExist):
                pass

            return Response(status=status.HTTP_200_OK)


class AtualizarUsuarioSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id',
                  'username',
                  'email',
                  'token',
                  'password'
                  ]
