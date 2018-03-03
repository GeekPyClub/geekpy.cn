import pickle
from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.shortcuts import redirect

# Create your views here.
from post.models import Post
from user.models import Users
from user.models import UsersSafety
from user.models import UsersInfo
from user.forms import RegisterForm
from user.forms import UserInfoForm


sexDict = {0: '保密', 1: '男', 2: '女'}


def myDeepCopy(obj):
    return pickle.loads(pickle.dumps(obj))


def login(request):
    # 验证是否登录
    userinfo = request.session.get('userinfo')
    if userinfo:
        return redirect('/user/info/')

    # 验证是否POST请求
    if not request.method == 'POST':
        msg = request.GET.get('warning')
        if msg == 'NoLogin':
            msg = '请先登录'
        elif msg == 'NotFunction':
            msg = '暂未开启找回密码功能'
        else:
            msg = '欢迎登陆'
        return render(request, 'user_login.html', {'warning_msgs': msg})

    username = request.POST.get('username')
    password = request.POST.get('password')

    # 用户是否存在
    try:
        user = Users.objects.get(username=username)
    except Users.DoesNotExist as e:
        return render(request, 'user_login.html', {'warning_msgs': '用户不存在'})

    # 密码是否正确
    if not user.checkout(password):
        return render(request, 'user_login.html', {'warning_msgs': '密码不正确'})

    # 用户信息是否存在
    try:
        userinfo = UsersInfo.objects.get(uid=user.id)    # 获取UserInfo对象
    except UsersInfo.DoesNotExist as e:
        userinfo = UsersInfo.objects.create(uid=user.id)    # 创建用户信息


    # 邮箱是否存在
    try:
        safey = UsersSafety.objects.get(uid=user.id)   # 获取UsersSafety对象
        useremail = safey.email
    except UsersSafety.DoesNotExist as e:
        useremail = '未填写'
    sexdict = myDeepCopy(sexDict)
    userinfo.sex = {sexdict.pop(int(userinfo.sex)): (int(userinfo.sex), sexdict)}   # 修改性别显示
    userinfo.username = username
    userinfo.email = useremail
    userinfo.created = user.created
    userinfo = dispose_icon(userinfo=userinfo)
    request.session['userinfo'] = userinfo

    # 是否激活(用来限制一些功能)
    request.session['active'] = True    # 关闭激活功能(无视数据库，默认激活)
    # request.session['active'] = user.active    # 开启激活功能(与数据库相关联)
    return redirect('/user/info/')


def logout(request):
    request.session.flush()
    return redirect('/index/')


def register(request):
    userinfo = request.session.get('userinfo')
    userinfo = dispose_icon(userinfo=userinfo)
    if userinfo:
        return redirect('/user/info/')

    if not request.method == 'POST':
        msg = '欢迎注册'
        form = RegisterForm()
        return render(request, 'user_register.html', {'form': form, 'warning_msgs': msg})

    form = RegisterForm(request.POST)
    try:
        # 校验数据
        if not form.is_valid():
            return render(request, 'user_register.html', {'warning_msgs': form.errors, 'form': form})
    except ValidationError as e:
        # 校验密码的自定义异常 'ValidationError'
        return render(request, 'user_register.html', {'warning_msgs': e, 'form': form})

    # 通过校验后开始注册逻辑
    username = form.cleaned_data.get('username')
    password = form.cleaned_data.get('password1')
    useremail = '未填写'
    try:
        # 用户名唯一
        Users.objects.get(username=username)
        return render(request, 'user_register.html', {'warning_msgs': '用户已存在', 'form': form})
    except Users.DoesNotExist as e:
        user = Users.objects.create(username=username, password=password)
        userinfo = UsersInfo.objects.create(uid=user.id)
        sexdict = myDeepCopy(sexDict)
        userinfo.sex = {sexdict.pop(int(userinfo.sex)): (int(userinfo.sex), sexdict)}    # 修改性别显示
        userinfo.email = useremail
        userinfo.username = username
        userinfo.created = user.created
        request.session['userinfo'] = userinfo
        request.session['register'] = True  # 是否注册
        # 设置激活(用来限制一些功能)
        request.session['active'] = True  # 关闭激活功能(无视数据库，默认激活)
        # request.session['active'] = user.active    # 开启激活功能(与数据库相关联)
        return redirect('/user/fill/?fill=%s' % (userinfo.nickname))



def fill_info(request):
    userinfo = request.session.get('userinfo')
    if not userinfo:
        return redirect('/user/login/?warning=NoLogin')

    # 验证是否注册流程
    is_register = request.session.get('register')
    if not is_register:
        return redirect('/user/edit/?warning=NoRegister')

    if not request.method == 'POST':
        form = UserInfoForm()
        form.nickname = userinfo.nickname
        return render(request, 'user_fill.html', {'form': form, 'userinfo': userinfo})

    form = UserInfoForm(request.POST, request.FILES)
    if not form.is_valid():
        return render(request, 'user_fill.html', {'form': form, 'warning_msgs': form.errors})

    # 调用函数处理数据UserInfo
    return dispose_info(request=request, userinfo=userinfo, form=form)


def dispose_info(request=None, userinfo=None, form=None):
    if not userinfo:
        userinfo = request.session.get('userinfo')
    # 获取UserInfo对象
    uid = userinfo.uid
    try:
        info = UsersInfo.objects.get(uid=uid)
    except UsersInfo.DoesNotExist as e:
        info = UsersInfo.objects.create(uid=uid)

    # 从POST请求中中获取相应数据
    email = request.POST.get('email')
    nickname = request.POST.get('nickname')
    icon = request.FILES.get('icon')
    birthday = request.POST.get('birthday')
    sex = request.POST.get('sex')
    signature = request.POST.get('signature')
    useremail = '未填写'
    if email:
        try:
            # 邮箱唯一，且在UsersSafety表中
            safety = UsersSafety.objects.get(email=email)
            if not int(safety.uid) == int(userinfo.uid):
                if not form:
                    return render(request, 'user_edit.html', {'warning_msgs': '邮箱已被注册'})
                return render(request, 'user_fill.html', {'form': form, 'warning_msgs': '邮箱已被注册'})

        except UsersSafety.DoesNotExist as e:
            # 创建UsersSafety对象
            safety = UsersSafety.objects.create(uid=uid, email=email)
            useremail = safety.email

    if nickname:
        try:
            # 昵称唯一，且在UsersInfo表中
            uinfo = UsersInfo.objects.get(nickname=nickname)
            if not int(uinfo.uid) == int(userinfo.uid):
                if not form:
                    render(request, 'user_edit.html', {'form': form, 'warning_msgs': '昵称已被注册'})
                return render(request, 'user_fill.html', {'form': form, 'warning_msgs': '昵称已被注册'})
        except UsersInfo.DoesNotExist as e:
            info.nickname = nickname

    # 非唯一属性，常规处理
    if icon:
        info.icon = icon
    if birthday:
        info.birthday = birthday
    if sex:
        info.sex = sex
    if signature:
        info.signature = signature
    info.save()

    # 保存UsersInfo对象后添加动态属性，存入session
    info.email = useremail
    info.username = userinfo.username
    info.created = userinfo.created
    sexdict = myDeepCopy(sexDict)
    info.sex = {sexdict.pop(int(info.sex)): (int(info.sex), sexdict)}  # 修改性别显示

    info = dispose_icon(userinfo=info)
    request.session['userinfo'] = info
    return redirect('/user/info/')


def edit_info(request):
    userinfo = request.session.get('userinfo')
    if not userinfo :
        return redirect('/user/login/?warning=NoLogin')

    if not request.method == 'POST':
        return render(request, 'user_edit.html', {'userinfo': userinfo})

    uid = request.POST.get('uid')
    if not int(uid) == int(userinfo.uid):
        return redirect('/user/login/?warning=NoLogin')

    return dispose_info(request=request, userinfo=userinfo)


def user_info(request, blog_pk=None):
    userinfo = request.session.get('userinfo')
    # 加工头像url
    userinfo = dispose_icon(userinfo=userinfo)
    print(3)
    # 显示公开的个人空间
    if blog_pk:
        blog = UsersInfo.objects.get(id=blog_pk)
        blog = dispose_icon(userinfo=blog)
        posts = Post.objects.filter(authid__exact=blog.id)[:10]
        return render(request, 'user_blog.html', {'posts': posts, 'blog': blog, 'userinfo': userinfo})

    # 显示登陆后的个人空间
    if not userinfo:
        return redirect('/user/login/?warning=NoLogin')

    return render(request, 'user_info.html', {'userinfo': userinfo})


def dispose_icon(userinfo=None):
    '''
    :param userinfo: 一个 包含用户信息的 object
    :return: 返回加工后的对象
    '''
    if userinfo:
        print(userinfo.icon,type(userinfo.icon), '1')
        # 如果是上传头像
        if str(userinfo.icon).startswith('upload'):
            userinfo.icon = "/media/%s" % (userinfo.icon)
        # 如果是默认头像
        if str(userinfo.icon).startswith('default'):
            userinfo.icon = "/static/%s" % (userinfo.icon)
    print(userinfo.icon, type(userinfo.icon), '2')
    return userinfo
