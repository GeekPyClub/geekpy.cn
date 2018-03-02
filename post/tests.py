import os

import django

from django.test import TestCase

# Create your tests here.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GeekPy.settings")
django.setup()
from post.models import Post


# 批量生成文章
title = 'The Zen of Python'
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

for i in range(1, 10):
    t = "%s-%d" % (title, i)
    Post.objects.create(title=t, body=post, uid=1, authid=1)