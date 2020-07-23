from django.db import models


# Create your models here.
class Publisher(models.Model):
    name = models.CharField(max_length=32)


class Book(models.Model):
    name = models.CharField(max_length=32)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    """
    on_delete  2.0版本后是必填的 
        models.CASCADE  级联删除
        models.PROTECT  保护
        models.SET(v)   删除后设置为某个值
        models.SETDEFAULT   删除后设置为默认值
        models.SET_NULL    删除后设置为Null
        models.DO_NOTHING  什么都不做
    """


class Author(models.Model):
    name = models.CharField(max_length=32)
    books = models.ManyToManyField('Book')


class User(models.Model):
    name = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
