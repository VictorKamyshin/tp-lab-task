from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User, UserManager
from datetime import datetime
from django.db.models import Count
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, verbose_name=u'User', related_name='users_profile')
    name = models.CharField(max_length=255, verbose_name=u'user name',null=False)
    surname = models.CharField(max_length=255, verbose_name=u'user surname', null=False)
    patronymic = models.CharField(max_length=255, verbose_name=u'user patronymic',null=False)
    email = models.CharField(max_length=255, verbose_name=u'user email', null=False, unique=True)
    avatar_url = models.CharField(max_length=255, verbose_name=u'avatar url', null=True)
    avatar = models.ImageField(upload_to='images',null=True)


class Film(models.Model):
    title = models.CharField(max_length=255, verbose_name=u'film title', null=False,
                             unique=True)
    description = models.CharField(max_length=4096, verbose_name=u'film description', null=True)
    premier = models.DateField(default=datetime.now, verbose_name=u'film premier date')
    rating = models.FloatField(null=True, verbose_name=u'film rating')
    count_of_appraisal = models.IntegerField(default=0, verbose_name=u'film count of appraisal')
    date_of_addition = models.DateField(default=datetime.now, verbose_name=u'film date of addition')
    isDeleted = models.BooleanField(default=False, verbose_name=u'film is deleted')
    count_of_root_comments = models.IntegerField(default=0, verbose_name=u'count of root comments')


class Appraisal(models.Model):
    value = models.IntegerField(null=False, verbose_name=u'appraisal value')
    author = models.ForeignKey(Profile,on_delete=models.CASCADE, verbose_name=u'appraisal author',
                               related_name=u'appraisal_author', null=False)
    film = models.ForeignKey(Film,on_delete=models.CASCADE, verbose_name=u'appraisal film',
                             related_name=u'appraisal_film', null=False)


class Comment(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name =u'comment author',
                               related_name=u'comment_author', null = False)
    film = models.ForeignKey(Film, on_delete=models.CASCADE, verbose_name=u'comment film', related_name=u'comment_film',
                             null=False)
    text = models.CharField(max_length=1024, verbose_name=u'comment text', null=True)
    material_path = models.CharField(max_length=40, verbose_name=u'material path', null = True)
    count_of_childs = models.IntegerField(default=0, verbose_name=u'count of childs')
    isDeleted = models.BooleanField(default=False)