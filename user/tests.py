import os

import django

from django.test import TestCase

# Create your tests here.
from post.models import Post

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GeekPy.settings")
django.setup()
from user.models import Users
from user.models import UsersInfo
from user.models import UsersSafety


title = 'Python之禅'
post = '''Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!'''


# 批量创建用户
usernames = ['geekpy', 'GeekPy', 'geekpy.cn', 'geekpycn', 'GeekPycn', 'GeekPy.cn',]
password = '123456'
signature = 'geekpy.cn官方账号'

for name in usernames:
    t = "%s-%s" % (title, name)
    email = '%s@geekpy.cn' % (name)
    nickname = '%s%s' % (signature, name)
    user = Users.objects.create(username=name, password=password)
    userInfo = UsersInfo.objects.create(uid=user.id, nickname=nickname, signature=signature)
    safetyEmail = UsersSafety.objects.create(uid=user.id, email=email)
    Post.objects.create(title=t, body=post, uid=user.id, authid=userInfo.id)