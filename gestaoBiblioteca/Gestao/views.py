from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from .serializers import (
    GeneroSerializer,
    AutorSerializer,
    LivroSerializer,
    )
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import(
    CreateAPIView,
    UpdateAPIView,
    ListAPIView)


class LivroCreateView (CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = LivroSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = LivroSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("Livro Salvo com sucesso", status=HTTP_200_OK)
        return Response("Erro no cadastramento do livro", status=HTTP_400_BAD_REQUEST)
