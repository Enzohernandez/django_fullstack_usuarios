import json
from builtins import object

from django import db
from django.core import serializers
from django.http import HttpResponse
from rest_framework.decorators import api_view
from api.models import Usuario, Post
from api.serializers import UsuarioDesserialized
from api.serializers import PostDesserialized
from django.db import IntegrityError


## OBTENCION DE USUARIOS Y COMENTARIOS USANDO GETS ##


@api_view(['GET'])
def get_usuarios(request):
    query_params = request.query_params  # obtener los parametros query del request
    user_id = query_params.get('id')  # obtener el id de los query_params
    user_usuario = query_params.get("usuarios")
    user_nombre = query_params.get("nombre")

    if user_nombre:
        try:
            user = Usuario.objects.filter(nombre=user_nombre)  # creando un objeto user y llamamos al id de user_id
            usuarios_as_json = serializers.serialize('json', user)  # serealizando el contenido
            return HttpResponse(usuarios_as_json, content_type='application/json')  # hacemos el return
        except Usuario.DoesNotExist:
            return HttpResponse("User not found", content_type='text/plain', status=404)  # 404 si usuario no existe
    if user_usuario:
        try:
            user = Usuario.objects.get(usuarios=user_usuario)  # creando un objeto user y llamamos al id de user_id
            usuarios_as_json = serializers.serialize('json', [user])  # serealizando el contenido
            return HttpResponse(usuarios_as_json, content_type='application/json')  # hacemos el return
        except Usuario.DoesNotExist:
            return HttpResponse("User not found", content_type='text/plain', status=404)  # 404 si usuario no existe
    if user_id:
        try:
            user = Usuario.objects.get(id=user_id)  # creando un objeto user y llamamos al id de user_id
            usuarios_as_json = serializers.serialize('json', [user])  # serealizando el contenido
            return HttpResponse(usuarios_as_json, content_type='application/json')  # hacemos el return
        except Usuario.DoesNotExist:
            return HttpResponse("User not found", content_type='text/plain', status=404)  # 404 si usuario no existe
    else:
        # si no se proporciona un id devolver todos los usuarios
        usuarios_as_json = serializers.serialize('json', Usuario.objects.all())
        return HttpResponse(usuarios_as_json, content_type='application/json')


@api_view(['GET'])
def get_posts(request):
    query_params = request.query_params
    user_id = query_params.get('user_id')  # hacemos lo mismo ya que el foreighn key nos permite relacionar ambas tablas
    user_titulo = query_params.get("titulo")
    user_descripcion = query_params.get("descripcion")
    id = query_params.get('id')
    if user_descripcion:
        try:
            user = Post.objects.filter(descripcion=user_descripcion)
            usuarios_as_json = serializers.serialize('json', user)
            return HttpResponse(usuarios_as_json, content_type='application/json')
        except Usuario.DoesNotExist:
            return HttpResponse("User not found", content_type='text/plain', status=404)
    if user_titulo:
        try:
            user = Post.objects.filter(titulo=user_titulo)
            usuarios_as_json = serializers.serialize('json', user)
            return HttpResponse(usuarios_as_json, content_type='application/json')
        except Usuario.DoesNotExist:
            return HttpResponse("User not found", content_type='text/plain', status=404)
    if user_id:
        try:
            objetoUsuario=Usuario()
            objetoUsuario.id=user_id
            postsbyUser = Post.objects.filter(usuarios=objetoUsuario)
            usuarios_as_json = serializers.serialize('json', postsbyUser)
            return HttpResponse(usuarios_as_json, content_type='application/json')
        except Usuario.DoesNotExist:
            return HttpResponse("User not found", content_type='text/plain', status=404)
    else:
        # If no 'id' provided, return all usuarios
        usuarios_as_json = serializers.serialize('json', Post.objects.all())
        return HttpResponse(usuarios_as_json, content_type='application/json')


## ELIMINACION DE USUARIOS EN USUARIOS Y POST MEDIANTE DELETE

@api_view(['DELETE'])
def eliminar_usuario(request):
    query_params = request.query_params  # obtener los query parameters de request
    user_id = query_params.get('id')  # obtener el id de los query parameters
    if not user_id:
        return HttpResponse("Please provide the 'id' parameter in the query.", content_type='text/plain', status=400)

    try:
        # Convercion del id a una integral
        user_id = int(user_id)

        # obtener el usuario con el id insertado
        usuario = Usuario.objects.get(id=user_id)

        # eliminarlo de la base de datos
        usuario.delete()

        return HttpResponse("User deleted successfully", content_type='text/plain', status=204)

    except ValueError:
        return HttpResponse("Invalid 'id' format. It should be an integer.", content_type='text/plain', status=400)
    except Usuario.DoesNotExist:
        return HttpResponse("User not found", content_type='text/plain', status=404)


@api_view(['DELETE'])
def eliminar_comentario(request):
    query_params = request.query_params  # obtener los query parameters de request
    user_id = query_params.get('id')  # obtener el id de los query parameters
    if not user_id:
        return HttpResponse("Please provide the 'id' parameter in the query.", content_type='text/plain', status=400)

    try:
        # Convercion del id a una integral
        user_id = int(user_id)

        # obtener el usuario con el id insertado
        usuario = Post.objects.get(id=user_id)

        # eliminarlo de la base de datos
        usuario.delete()

        return HttpResponse("User deleted successfully", content_type='text/plain', status=204)

    except ValueError:
        return HttpResponse("Invalid 'id' format. It should be an integer.", content_type='text/plain', status=400)
    except Post.DoesNotExist:
        return HttpResponse("User not found", content_type='text/plain', status=404)


## CREACION DE USUARIOS Y POSTS USANDO POST ##


@api_view(['POST'])
def sign_in(request):
    creacion_usuario = Usuario()  # creacion de objeto
    creacion_usuario.usuarios = request.data["usuarios"]  # obteniendo los datos para cada uno
    creacion_usuario.nombre = request.data["nombre"]
    creacion_usuario.correo = request.data["correo"]
    creacion_usuario.contrasena = request.data["contrasena"]
    creacion_usuario.save()  # guradando_todo
    db.connections.close_all()  # cerrando conecciones con la base de datos
    return HttpResponse(serializers.serialize('json', [creacion_usuario, ]), content_type='application/json')


@api_view(['POST'])
def sign_in_nuevo(request):
    try:
        creacion_usuario = Usuario()  # creacion de objeto
        creacion_usuario.usuarios = request.data["usuarios"]  # obteniendo los datos para cada uno
        creacion_usuario.nombre = request.data["nombre"]
        creacion_usuario.correo = request.data["correo"]
        creacion_usuario.contrasena = request.data["contrasena"]
        creacion_usuario.save()  # guradando_todo
        db.connections.close_all()  # cerrando conecciones con la base de datos
        return HttpResponse(serializers.serialize('json', [creacion_usuario, ]), content_type='application/json')

    except IntegrityError as e:
        if 'unique constraint' in str(e).lower() and 'correo' in str(e).lower():
            return HttpResponse("Usuario con este email ya existe", content_type='text/plain', status=409)
        else:
            return HttpResponse("Ocurrio un error mientras se procesaba su solicitud", content_type='text/plain',
                                status=500)


@api_view(['POST'])
def postear_comentario(request):
    creacion_post = Post()
    creacion_post.titulo = request.data["Titulo"]
    creacion_post.descripcion = request.data["Descripcion"]
    usuario_related = Usuario()
    usuario_related.id = request.data["Usuarios_ID"]
    creacion_post.usuarios = usuario_related
    creacion_post.save()
    db.connections.close_all()
    return HttpResponse(serializers.serialize('json', [creacion_post, ]), content_type='application/json')


@api_view(['POST'])
def desactivar_usuario(request):
    query_params = request.query_params
    user_id = query_params.get('id')
    try:
        user_id = int(user_id)
        usuario = Usuario.objects.get(id=user_id)
        usuario.activo = False
        usuario.save()
        return HttpResponse("Usuario desactivado correctamente.", content_type='text/plain', status=200)
    except Usuario.DoesNotExist:
        return HttpResponse("Usuario no encontrado.", content_type='text/plain', status=404)


## MODIFICACION DE USUARIOS Y POSTS USANDO PUT ##

@api_view(['PUT'])
def modificar_usuario(request):
    query_params = request.query_params
    user_id = query_params.get('id')

    if not user_id:
        return HttpResponse("Please provide the 'id' parameter in the query.", content_type='text/plain', status=400)

    try:
        user_id = int(user_id)  # convercion a integral
        usuario = Usuario.objects.get(id=user_id)  # asociando el id con el objeto
        updated_data = json.loads(request.body)  # abstrayendo la info de put de postman
        serializer = UsuarioDesserialized(usuario, data=updated_data)  # serializando la informacion
        if serializer.is_valid():
            serializer.save()
            return HttpResponse("User updated successfully", content_type='text/plain', status=200)
        else:
            return HttpResponse(serializer.errors, content_type='application/json', status=400)

    except ValueError:
        return HttpResponse("Invalid 'id' format. It should be an integer.", content_type='text/plain', status=400)
    except Usuario.DoesNotExist:
        return HttpResponse("User not found", content_type='text/plain', status=404)


@api_view(['PUT'])
def modificar_post(request):
    query_params = request.query_params
    post_id = query_params.get('id')

    if not post_id:
        return HttpResponse("Please provide the 'id' parameter in the query.", content_type='text/plain', status=400)

    try:
        post_id = int(post_id)
        post = Post.objects.get(id=post_id)
        updated_data = json.loads(request.body)
        serializer = PostDesserialized(post, data=updated_data)
        # if updated_data["title"]:
        #     post.titulo=updated_data["title"]
        # if updated_data["description"]:
        #     post.descripcion = updated_data["description"]
        if serializer.is_valid():
            serializer.save()
            return HttpResponse("Post updated successfully", content_type='text/plain', status=200)
        else:
            return HttpResponse(serializer.errors, content_type='application/json', status=400)

    except ValueError:
        return HttpResponse("Invalid 'id' format. It should be an integer.", content_type='text/plain', status=400)
    except Post.DoesNotExist:
        return HttpResponse("Post not found", content_type='text/plain', status=404)
