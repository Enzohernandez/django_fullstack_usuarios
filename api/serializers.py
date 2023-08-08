from rest_framework import serializers
from .models import Usuario
from.models import Post


class UsuarioDesserialized(serializers.ModelSerializer):
    usuarios = serializers.CharField(max_length=250)

    class Meta:
        model = Usuario
        fields = ('__all__')


class PostDesserialized(serializers.ModelSerializer):
    Titulo = serializers.CharField(max_length=250, source="titulo")
    descripcion = serializers.CharField(max_length=250,source="titulo")
    class Meta:
        model = Post
        fields = ('other_fields', 'location')
