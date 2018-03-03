import time
import random
from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password

# Create your models here.

timeNow = time.time()
dateNow = time.strftime('%Y-%m-%d', time.localtime(timeNow))
rid = random.randint(1,100)
defaultname = '会员%d%d%d' % (timeNow, rid, rid)


class Users(models.Model):
    username = models.CharField(max_length=64, verbose_name='用户名', unique=True, blank=False, null=False)
    password = models.CharField(max_length=64, verbose_name='密码', blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True, verbose_name='注册时间')
    active = models.BooleanField(default=False)

    def checkout(self, password):
        return check_password(password, self.password)

    def save(self, *args, **kwargs):
        if not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save()


class UsersSafety(models.Model):
    uid = models.IntegerField(verbose_name='用户id', unique=True, blank=False, null=False)
    email = models.EmailField(unique=True, verbose_name='邮箱')


class UsersInfo(models.Model):
    uid = models.IntegerField(verbose_name='用户id', unique=True, blank=False, null=False)
    nickname = models.CharField(max_length=64, unique=True, verbose_name='昵称', default=defaultname)
    icon = models.ImageField(upload_to='upload/icon/%Y/%m/%d',
                             default='defaultMedia/icon/0.jpg', verbose_name='头像')
    birthday = models.CharField(max_length=16, verbose_name='生日', default=dateNow)
    sex = models.IntegerField(choices=((0, '保密'), (1, '男'), (2, '女')), default=0)
    signature = models.CharField(max_length=128, verbose_name='简介', default='这家伙什么也没写')
