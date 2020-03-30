from django.conf.urls import url
from .views import (LivroCreateView)

urlpatterns = [
    url(r'^cadastrarLivro/$', LivroCreateView.as_view(), name='cadastrarLivro'),
]