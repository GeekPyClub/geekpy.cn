from django.shortcuts import render
from django.shortcuts import redirect

# Create your views here.
from post.models import Post
from post.helper import paging
from post.forms import createForm

# 提示文章找不到，因为用得比较多，所以单独提取出来。
not_find_warning = {'warning_msgs': '文章找不到'}


def post_read(request, post_pk=0):
    # 获取session
    userinfo = request.session.get('userinfo')
    # 将session更新到 not_find_warning字典中, 生成上下文字典
    not_find_context = dict(not_find_warning, **{'userinfo': userinfo})

    if not post_pk:
        return render(request, 'post_read.html', not_find_context)

    try:
        post = Post.objects.get(id=post_pk)
        # 无处不在的{‘userinfo’: userinfo}, 是为了给前端传递用户数据
        info_context = {'post': post, 'userinfo': userinfo}
        return render(request, 'post_read.html', info_context)
    except Post.DoesNotExist:
        # 如果文章不存在，提示找不到
        return render(request, 'post_read.html', not_find_context)


def post_list(request):
    msg = '欢迎光临'
    userinfo = request.session.get('userinfo')

    # print(type(request.GET.get('page', 1)), request.GET.get('page', 1))    # 测试用
    getPage = request.GET.get('page', 1)

    # 有时候会取到一个空字符串，而不是默认值的 1
    if not str(getPage).isdigit():
        getPage = 1
    getPage = int(getPage)
    pageCount = 10
    pageShow = 4
    postMax = int(Post.objects.count())
    # 分页功能所需参数
    postBegin, postEnd, thePage, pageMax, pages = paging(thePage=getPage, pageShow=pageShow,
                                                         pageCount=pageCount, postMax=postMax)
    posts = Post.objects.all()[postBegin: postEnd]
    context = {'posts': posts, 'pages': pages, 'pageMax': pageMax, 'thePage': thePage,
               'warning_msgs': msg, 'userinfo': userinfo}
    return render(request, 'post_list.html', context)


def post_add(request):
    userinfo = request.session.get('userinfo')

    # 是否登录
    if not userinfo:
        return redirect('/user/login/?warning=NoLogin')

    # 是否激活
    if not request.session.get('active'):
        return render(request, 'post_add.html', {'warning_msgs': '请先验证邮箱激活账号', 'userinfo': userinfo})

    if not request.method == 'POST':
        form = createForm()
        context = {'form': form, 'userinfo': userinfo}
        return render(request, 'post_add.html', context)

    form = createForm(request.POST)
    title = request.POST.get('title')
    body = request.POST.get('body')

    context = {'warning_msgs': '发表成功', 'userinfo': userinfo, 'form': form}
    if not title:
        msg = '请输入标题'
        context['warning_msgs'] = msg
        return render(request, 'post_add.html', context)

    if not body:
        msg = '请输入正文'
        context['warning_msgs'] = msg
        return render(request, 'post_add.html', context)

    try:
        # 判断同名文章是否存在, title 唯一。
        post = Post.objects.get(title=title)
        msg = '同名文章已存在, 请修改标题'
        context['warning_msgs'] = msg
        return render(request, 'post_add.html', context)
    except Post.DoesNotExist:
        post = Post.objects.create(title=title, body=body, uid=userinfo.uid, authid=userinfo.id)

    return redirect('/post/read/%s' % (post.id))


def post_edit(request, post_pk=0):
    userinfo = request.session.get('userinfo')
    not_find_context = dict(not_find_warning, **{'userinfo': userinfo})
    if not userinfo:
        return redirect('/user/login/?warning=NoLogin')

    if not request.session.get('active'):
        context = {'warning_msgs': '请先验证邮箱激活账号', 'userinfo': userinfo}
        return render(request, 'post_edit.html', context)

    # 处理非POST(非编辑)请求
    if not request.method == 'POST':
        post_id = int(post_pk)
        if post_id == 0:
            return render(request, 'post_edit.html', not_find_context)

        # 提取文章
        try:
            post = Post.objects.get(id=post_id)
            context = {'post': post, 'userinfo': userinfo}
            return render(request, 'post_edit.html', context)
        except Post.DoesNotExist as e:
            return render(request, 'post_edit.html', not_find_context)

    # 正常编辑流程
    post_id = int(request.POST.get('post_id', 0))
    if post_id == 0:
        return render(request, 'post_edit.html', not_find_context)

    # 提取文章
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist as e:
        return render(request, 'post_edit.html', not_find_context)

    # 判断权限(目前只有作者能编辑)
    if not userinfo.id == post.authid:
        context = {'userinfo': userinfo, 'warning_msgs': '没有权限'}
        return render(request, 'post_edit.html', context)

    title = request.POST.get('title')
    body = request.POST.get('body')

    # 有改动则更新
    if not post.title == title:
        post.title = title

    if not post.body == body:
        post.body = body

    # 保存
    post.save()
    return redirect('/post/read/%s' % (post.id))
