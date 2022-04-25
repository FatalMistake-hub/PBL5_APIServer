from django.db import models

# Create your models here.

class Image_recognize(models.Model):
    name = models.CharField(max_length=50)
    Image_recognize_main = models.ImageField(upload_to='images/')

    
class Users(models.Model):
    user_id = models.AutoField(
        primary_key=True, null=False, editable=False, unique=True
    )
    full_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=20, null=True)
    gender = models.CharField(max_length=10, null=True)
    birthday = models.DateField(null=True)
    face_vectors = models.TextField(null=True)

    def __str__(self):
        return str(self.user_id)
class Door(models.Model):
    name = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    time = models.DateField(null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Door'
