from django.conf.urls import url
from .views import (LoginView,
                    LogOutView,
                    UserListViewAll,
                    UserCreateView,
                    ChangePasswordView)

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogOutView.as_view(), name='logout'),
    url(r'^listar/$', UserListViewAll.as_view(), name='listar'),
    url(r'^cadastro/$', UserCreateView.as_view(), name='cadastro'),
    url(r'^torcarSenha/$', ChangePasswordView.as_view(), name='trocarSenha'),
]