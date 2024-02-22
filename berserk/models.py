from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from berserk.validators.validator_name import Validator_name
from berserk.validators.validator_password import Validator_passwod
#класс модели под создание записей (название модели соответствует её роли)
class br(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_posts')
    title = models.CharField(max_length=33) #заголовок
    content = models.TextField(max_length=250) #содержание записи
    published = models.DateTimeField(db_index=True, auto_now_add=True) #время публикации 
    

#класс модели под регистрацию
class AdvUser(AbstractUser):
    email = models.EmailField(unique=True,blank=False, null=False,verbose_name="Email Address")
    username = models.TextField(max_length=33, blank=True, null=True, verbose_name="Username",unique=True, validators=[Validator_name])
    password = models.CharField(default=None, max_length=25,blank=True, null=True, validators=[Validator_passwod])

#реализация комментирования под записями 
class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey('berserk.br', on_delete=models.CASCADE)
    text = models.TextField(max_length=250)
    created_at = models.DateTimeField(default=timezone.now)


#реализация оценивания записей 
class RecordLike(models.Model):
    like = models.IntegerField( default=0, validators=[MinValueValidator(-999999999999),  
            MaxValueValidator(999999999999),],)
    post = models.ForeignKey(br, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,  on_delete=models.CASCADE)


#дополнительная информация о пользователе
class ExtraInformation(models.Model):
    CHOICES = (
        (True, 'Male'),
        (False, 'Female'),
    )
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='user_images/',blank=True, null=True)
    e_inf = models.TextField(default=None, max_length=75, blank=True, null=True)
    age = models.DateField(default=None, blank=True,null=True,)
    gender = models.BooleanField(default=None,choices=CHOICES, blank=True, null=True)


class SerarchRecord(models.Model):
    value = models.CharField(default=None, blank=True,max_length=25,verbose_name="Search")

class ImagesAdmin(models.Model):
    image = models.ImageField(upload_to='user_images/',blank=True, null=True)


#после каждого изменения моделей обязательно 
#python manage.py makemigrations
#python manage.py migrate 
