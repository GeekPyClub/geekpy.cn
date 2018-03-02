import random
from django.db import models

# Create your models here.
from django.utils.html import strip_tags

from user.models import UsersInfo
randNum = random.randint(100, 999)

class Post(models.Model):
    uid = models.IntegerField(verbose_name='账户id', blank=False, null=False)    # Users表 证明归属
    authid = models.IntegerField(verbose_name='用户id', blank=False, null=False)    # UsersInfo表 提取作者信息
    title = models.CharField(max_length=200, unique=True, verbose_name='标题', blank=False, null=False)
    body = models.TextField(verbose_name='正文')
    modified = models.DateTimeField(auto_now=True, verbose_name='修改时间')
    excerpt = models.CharField(max_length=300, null=True, blank=True, verbose_name='摘要')
    created = models.DateTimeField(auto_now_add=True, verbose_name='发表时间')

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = '文章'
        ordering = ['-created']

    def __str__(self):
        return self.title

    @property
    def auth(self):
        if not hasattr(self, '_auth'):
            # 将 _auth 缓存为 self 的属性 (对象级别缓存)
            self._auth = UsersInfo.objects.get(id=self.authid)
        return self._auth


    def save(self, *args, **kwargs):
        if not self.title:
            # 因title具有唯一性，如果参数缺少title，则给一个相对复杂的默认值。
            self.title = "%s 来自:%s-%s%s%s%s" % (strip_tags(self.body)[5], self.auth.nickname,
                                               self.id, self.uid, self.authid, randNum)
        if not self.excerpt:
            self.excerpt = strip_tags(self.body)[:64]
        super(Post, self).save(*args, **kwargs)