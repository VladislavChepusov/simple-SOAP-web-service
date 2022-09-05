from django.contrib.auth.models import AbstractUser
from django.db import models
# from django.utils.translation import ugettext_lazy as _
from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = models.CharField(max_length=40, unique=True)
    email = models.EmailField('email', unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Article(models.Model):
    title = models.CharField(unique=True,max_length=255, verbose_name="Заголовок")
    content = models.TextField(blank=True, verbose_name="Текст статьи")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    is_private = models.BooleanField(default=False, verbose_name="Сделать приватной")
    author = models.ForeignKey(CustomUser, verbose_name='Автор', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    # def get_absolute_url(self):
    #     return reverse('post', kwargs={'post_id': self.pk})

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'
        ordering = ['id']
