from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer, ValidationError, EmailField, CharField, Serializer

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from .models import (Genero,Autor,Livro,Locacao)

User = get_user_model()


class GeneroSerializer(ModelSerializer):

    class Meta:
        model = Genero
        fields = ['descGenero',
                  'usuarioCadastro',
                  'usuarioEdicao',
                  'dtCadastro',
                  'dtedicao'
                  ]


class AutorSerializer(ModelSerializer):

    class Meta:
        model = Autor
        fields = ['nomeAutor',
                  'usuarioCadastro',
                  'usuarioEdicao',
                  'dtCadastro',
                  'dtEdicao'
                  ]


class LivroSerializer(ModelSerializer):

    class Meta:
        model = Livro
        fields = ['nomeLivro',
                  'autor',
                  'genero',
                  'usuarioCadastro',
                  'usuarioEdicao',
                  'dtCadastro',
                  'dtedicao'
                  ]


class LocacaoSerializer(ModelSerializer):

    class Meta:
        model = Locacao
        fields = ['livro',
                  'usuarioCadastro',
                  'dtCadastro'
                  ]
