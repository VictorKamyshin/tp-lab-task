from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User, UserManager
from datetime import datetime
from django.db.models import Count
from django.db import models

max_depth = 5


class Profile(models.Model):
    user = models.OneToOneField(User, verbose_name=u'User', related_name='users_profile')
    name = models.CharField(max_length=255, verbose_name=u'user name',null=False)
    surname = models.CharField(max_length=255, verbose_name=u'user surname', null=False)
    patronymic = models.CharField(max_length=255, verbose_name=u'user patronymic',null=False)
    email = models.CharField(max_length=255, verbose_name=u'user email', null=False, unique=True)
    avatar_url = models.CharField(max_length=255, verbose_name=u'avatar url', null=True, blank=True)
    avatar = models.ImageField(upload_to='images', null=True, blank=True)


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


class AppraisalManager(models.Manager):
    def user_appraisal(self, user_id):
        return self.filter(author__id=user_id)

    def film_appraisal(self, film_id):
        return self.filter(film__id=film_id)

    def film_appraisal_distribution(self, film_id):
        return self.filter(film__id=film_id).values('value').annotate(count=Count('value'))

    def user_appraisal_distribution(self, user_id):
        return self.filter(author__id=user_id).values('value').annotate(count=Count('value'))


class Appraisal(models.Model):
    value = models.IntegerField(null=False, verbose_name=u'appraisal value')
    author = models.ForeignKey(Profile,on_delete=models.CASCADE, verbose_name=u'appraisal author',
                               related_name=u'appraisal_author', null=False)
    film = models.ForeignKey(Film,on_delete=models.CASCADE, verbose_name=u'appraisal film',
                             related_name=u'appraisal_film', null=False)
    customManager = AppraisalManager()


class CommentManager(models.Manager):
    def create_comment(self, text, author, parent, film):
        if parent is None:
            film.count_of_root_comments += 1
            film.save()
            list_path = list('a'*max_depth)
            list_path[0] = chr(ord(list_path[0])+film.count_of_root_comments)
            path = ''.join(list_path)
            comment = self.create(author=author,film=film,text=text,material_path=path)
            return comment
        else:
            parent.count_of_childs += 1
            parent.save()
            list_path = list(parent.material_path)
            if parent.level != (max_depth-1):
                list_path[parent.level+1] = chr(ord(list_path[parent.level+1])+parent.count_of_childs)
                path = ''.join(list_path)
                comment = self.create(author=author, film=film, text=text, material_path=path, level=parent.level+1)
            else:
                list_path[parent.level] = chr(ord(list_path[parent.level])+parent.count_of_childs)
                path = ''.join(list_path)
                comment = self.create(author=author, film=film, text=text, material_path=path, level=parent.level)
            return comment


class Comment(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name =u'comment author',
                               related_name=u'comment_author', null = False)
    film = models.ForeignKey(Film, on_delete=models.CASCADE, verbose_name=u'comment film', related_name=u'comment_film',
                             null=False)
    text = models.CharField(max_length=1024, verbose_name=u'comment text', null=True)
    material_path = models.CharField(max_length=10, default='a'*max_depth, verbose_name=u'material path', null = False)
    count_of_childs = models.IntegerField(default=0, verbose_name=u'count of childs')
    isDeleted = models.BooleanField(default=False)
    level = models.IntegerField(default=0, verbose_name=u'level of depth of comment')

    customManager = CommentManager()