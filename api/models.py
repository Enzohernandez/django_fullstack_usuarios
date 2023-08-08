from django.db import models

class Usuario(models.Model):

    usuarios = models.CharField(max_length=250)
    nombre = models.CharField(max_length=250)
    correo = models.EmailField()
    contrasena = models.CharField(max_length=250)
#   activo = models.BooleanField(default=True)

    class Meta:
        managed = False
        db_table = "usuarios"

class Post(models.Model):
    title = models.CharField(max_length=250,db_column="Titulo")
    description = models.CharField(max_length=250,db_column="Descripcion")
    usuarios = models.ForeignKey(Usuario, on_delete=models.CASCADE) #objeto de tipo usuario

    class Meta:
        managed = True
        db_table = "post"

