from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from .serializers import (
    UserListarSerializer,
    LogoutSerializer,
    LoginSerializer,
    CadastroUsuarioSerializer,
    AtualizarUsuarioSerializer
    )
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import(
    CreateAPIView,
    UpdateAPIView,
    ListAPIView)

User = get_user_model()


class UserCreateView (CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = CadastroUsuarioSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        if User.objects.filter(username = request.data['username']).exists():
            return Response('Usuário já cadastrado com o username', status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=request.data['email']).exists():
            return Response('O e-mail informado já foi cadastrado no sistema.', status=status.HTTP_400_BAD_REQUEST)

        serializer = CadastroUsuarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("Usuário salvo com sucesso", status=HTTP_200_OK)
        return Response("Erro no cadastramento do usuário", status=HTTP_400_BAD_REQUEST)


class UserListViewAll (ListAPIView):
   # permission_classes = [AllowAny]
    serializer_class = UserListarSerializer
    queryset = User.objects.all()
    pagination_class = None


class LoginView(APIView):

    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = LoginSerializer(data=data)
        if serializer.is_valid():
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class LogOutView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = LogoutSerializer(data=data)
        if serializer.sair(data):
            return Response("Saiu com sucesso", status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class ChangePasswordView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AtualizarUsuarioSerializer

    def update(self, request, *args, **kwargs):
        usuario_update = User.objects.get(username=self.request.user.username)
        if request.data['password_new'] == "":
            return Response("Favor digitar a senha nova", status=HTTP_400_BAD_REQUEST)
        if request.data['password_old'] == "":
            return Response("Favor digitar a senha velha", status=HTTP_400_BAD_REQUEST)
        if request.data['password_new'] == request.data['password_old']:
            return Response("As senha nova deve ser diferente da sua senha antiga", status=HTTP_400_BAD_REQUEST)
        if usuario_update.check_password(request.data['password_old']):
            usuario_update.set_password(request.data['password_new'])
            usuario_update.save()
            return Response("Senha mudada com sucesso", status=HTTP_200_OK)
        return Response("A senha digitada é invalida", status=HTTP_400_BAD_REQUEST)


