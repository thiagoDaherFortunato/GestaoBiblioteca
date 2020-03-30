from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


class Genero(models.Model):
    descGenero = models.CharField(max_length=45, verbose_name='DescNomeCliente')
    usuarioCadastro = models.ForeignKey(User, models.PROTECT, null=False, blank=False, related_name='UsuarioCadastro',
                                verbose_name='Usuario')
    usuarioEdicao = models.ForeignKey(User, models.PROTECT, null=False, blank=False, related_name='UsuarioEdicao',
                                        verbose_name='Usuario')
    dtCadastro = models.DateTimeField(blank=True, null=True, default=timezone.now, verbose_name='Data de cadastro')
    dtEdicao = models.DateTimeField(blank=True, null=True, default=timezone.now, verbose_name='Data da última edição')

    class Meta:
        db_table = 'Genero'

    def __str__(self):
        return self.descGenero


class Autor(models.Model):
    nomeAutor = models.CharField(max_length=45, verbose_name='DescNomeCliente')
    usuarioCadastro = models.ForeignKey(User, models.PROTECT, null=False, blank=False, related_name='UsuarioCadastroAutor',
                                verbose_name='Usuario')
    usuarioEdicao = models.ForeignKey(User, models.PROTECT, null=False, blank=False, related_name='UsuarioEdicaoAutor',
                                        verbose_name='Usuario')
    dtCadastro = models.DateTimeField(blank=True, null=True, default=timezone.now, verbose_name='Data de cadastro')
    dtEdicao = models.DateTimeField(blank=True, null=True, default=timezone.now, verbose_name='Data da última edição')

    class Meta:
        db_table = 'Autor'

    def __str__(self):
        return self.nomeAutor


class Livro(models.Model):
    nomeLivro = models.CharField(max_length=45, verbose_name='DescNomeCliente')
    autor = models.ForeignKey(Autor, models.PROTECT, null=False, blank=False, related_name='Autor', verbose_name='Autor')
    genero = models.ForeignKey(Genero, models.PROTECT, null=False, blank=False, related_name='Genero', verbose_name='Genero')
    usuarioCadastro = models.ForeignKey(User, models.PROTECT, null=False, blank=False, related_name='UsuarioCadastroLivro',
                                verbose_name='Usuario')
    usuarioEdicao = models.ForeignKey(User, models.PROTECT, null=False, blank=False, related_name='UsuarioEdicaoLivro',
                                        verbose_name='Usuario')
    dtCadastro = models.DateTimeField(blank=True, null=True, default=timezone.now, verbose_name='Data de cadastro')
    dtEdicao = models.DateTimeField(blank=True, null=True, default=timezone.now, verbose_name='Data da última edição')

    class Meta:
        db_table = 'Livro'

    def __str__(self):
        return self.nomeLivro


class Locacao(models.Model):
    livro = models.ManyToManyField(Livro)
    usuarioCadastro = models.ForeignKey(User, models.PROTECT, null=False, blank=False, related_name='UsuarioCadastroLocacao',
                                verbose_name='Usuario')
    dtCadastro = models.DateTimeField(blank=True, null=True, default=timezone.now, verbose_name='Data de cadastro')


    class Meta:
        db_table = 'Locacao'

    def __str__(self):
        return self.livro
