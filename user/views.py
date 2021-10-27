import datetime
import pytz
from uuid import uuid4
from movie_web import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from user.models import User, History, ConfirmString, UserComment
from movie.models import DouBanMovie, Movie
from django.core.exceptions import ObjectDoesNotExist
from user.utils import ItemCF
from django.db.models import Q


# 注册用户
def register(request):
    username = request.POST['Username']
    password = request.POST['Password']
    sex = request.POST['Sex']
    age = request.POST['Age']
    email = request.POST['Email']
    try:
        user = User.objects.get(username=username)
        messages.error(request, "账号已经存在,换个账号试试吧!")
        return redirect('/movie/index')
    except:
        try:
            user = User.objects.get(email=email)
            messages.error(request, "该邮箱已注册，请更改邮箱!")
            return redirect('/movie/index')
        except:
            user = User(username=username, password=password, sex=sex, age=age, email=email)
            user.save()
            code = make_confirm_string(user)
            # 使用django来获取用户访问的IP地址 request.META['REMOTE_ADDR']
            send_email(request.META['REMOTE_ADDR'], email, code)
            message = '请前往注册邮箱，进行邮件确认！'
            # locals() 函数会以字典类型返回当前位置的全部局部变量。
            return render(request, 'user/confirm.html', locals())


# 生成验证码
def make_confirm_string(user):
    code = str(uuid4())
    ConfirmString.objects.create(code=code, user=user)
    return code


# 发送邮件
def send_email(ip, email, code):
    from django.core.mail import EmailMultiAlternatives

    subject = '来自猜你喜欢电影网站注册确认邮件'  # 邮件主题

    text_content = '''欢迎注册猜你喜欢电影网站，专注于提供各种影视的观看和推荐！\
                        如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！'''  # 邮件文本内容

    html_content = '''
                        <p>感谢注册猜你喜欢电影网站，请点击<a href="http://{}/user/confirm?code={}" target=blank>确认注册</a>，\
                        <p>请点击站点链接完成注册确认！</p>
                        <p>此链接有效期为{}天！</p>
                        '''.format(ip + ':8000', code, settings.CONFIRM_DAYS)  # 邮件html内容，可以加入css,js等

    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


# 进行注册验证
def user_confirm(request):
    # 从验证链接中获取验证码
    code = request.GET.get('code', None)
    message = ''
    try:
        # 获取验证码对象
        confirm = ConfirmString.objects.get(code=code)
    except:
        # 若对象不存在，则验证码无效
        message = '无效的确认请求!'
        return render(request, 'user/confirm.html', locals())

    c_time = confirm.c_time
    now = datetime.datetime.now()
    now = now.replace(tzinfo=pytz.timezone('UTC'))
    # 判断当前时间是否超过了发验证码后的7天
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.user.delete()
        message = '您的邮件已经过期！请重新注册!'
        return render(request, 'user/confirm.html', locals())
    else:
        confirm.user.is_checked = 1
        confirm.user.save()
        confirm.delete()
        message = '恭喜您注册成功，赶快尝试登录吧！'
        return render(request, 'user/confirm.html', locals())


# 用户登录
def login(request):
    # 后期用装饰器或中间键优化
    if 'Username' in request.POST.keys():
        username = request.POST['Username']
    else:
        return redirect('/movie/index')
    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        user = None
    if user:
        if user.is_checked == '0':
            messages.error(request, "该用户未激活，请去邮箱中激活后使用！")
        else:
            if user.password == request.POST['Password']:
                request.session['username'] = user.username
            else:
                messages.error(request, "密码错误！")
    else:
        messages.error(request, "用户不存在！")
    return redirect('/movie/index')


# 用户注销
def logout(request):
    # 清除当前对应session所有数据
    request.session.clear()
    # 重定向到主页
    return redirect('/movie/index')


# personal_index 用户主页
def personal_index(request):
    if 'username' in request.session.keys():
        username = request.session['username']
        user = User.objects.get(username=username)
        all_type = {}  # 记录各种类型电影观看次数
        histories = History.objects.filter(username=username)
        for history in histories:
            if history.tag == '0':
                movie = DouBanMovie.objects.get(id=history.video_id)
            else:
                movie = Movie.objects.get(id=history.video_id)
            all_type[movie.type] = all_type.setdefault(movie.type, 0) + 1
        return render(request, 'user/index.html', {'user': user, 'movie_type': all_type.items()})
    else:
        messages.error(request, "请登录后再操作！")
        return redirect('/movie/index')


# personal_info 个人信息
def personal_info(request):
    if 'username' in request.session.keys():
        username = request.session['username']
        user = User.objects.get(username=username)
        return render(request, 'user/userInfo.html', {'user': user})
    else:
        messages.error(request, "请登录后再操作！")
        return redirect('/movie/index')


# 显示观看历史记录
def personal_history(request):
    history_info = {}
    if 'username' in request.session.keys():
        username = request.session['username']
        user = User.objects.get(username=username)
        histories = History.objects.filter(username=username)
        num = histories.count()
        for history in histories:
            if history.tag == '0':
                history_info[history.current_time] = DouBanMovie.objects.get(id=history.video_id)
            else:
                history_info[history.current_time] = Movie.objects.get(id=history.video_id)
        history_info = sorted(history_info.items(), key=lambda x: x[0], reverse=True)
        return render(request, 'user/history.html', {'num': num,
                                                     'user': user, 'history_info': history_info})
    else:
        messages.error(request, "请登录后再操作！")
        return redirect('/movie/index')


# 删除指定历史记录
def delete_history(request, get_time):
    history = History.objects.filter(current_time=get_time)
    history.delete()
    return redirect('/user/personal_history')


# 修改密码
def modify_info(request):
    username = request.POST.get('username')
    user = User.objects.get(username=username)
    if 'new_pass' in request.POST.keys():
        new_pass = request.POST.get('new_pass')
        user.password = new_pass
    if 'email' in request.POST.keys():
        email = request.POST.get('email')
        user.email = email
    user.save()
    return JsonResponse({'res': 1})


# 显示电影评分列表
def show_evaluate(request):
    evaluate_info = {}
    if 'username' in request.session.keys():
        username = request.session['username']
        user = User.objects.get(username=username)
        histories = History.objects.filter(username=username)
        for history in histories:
            if history.tag == '0':
                movie = DouBanMovie.objects.get(id=history.video_id)
                evaluate_info[movie.name] = [history.current_time, history.evaluate_star, movie]
            else:
                movie = Movie.objects.get(id=history.video_id)
                evaluate_info[movie.name] = [history.current_time, history.evaluate_star, movie]
        num = len(evaluate_info)
        return render(request, 'user/evaluate_movie.html', {'num': num,
                                                            'user': user, 'evaluate_info': evaluate_info.values()})
    else:
        messages.error(request, "请登录后再操作！")
        return redirect('/movie/index')


# 对观看电影进行评分
def mark_movie(request):
    star = request.GET.get('star')
    history = History.objects.get(current_time=request.GET.get('time'))
    history.evaluate_star = star
    history.save()
    return JsonResponse({'res': 1})


# 显示推荐电影
def recommend_movie(request):
    flag = 0  # 默认为系统推荐
    if 'username' in request.session.keys():
        username = request.session['username']
        user = User.objects.get(username=username)
        # 推荐的电影或电视列表
        movies = []
        data = History.objects.all().exclude(evaluate_star='')
        recommend_list = ItemCF.get_recommend(data, user.username)
        if len(recommend_list) == 0:
            movie_type = {}  # 记录各种类型电影观看次数
            histories = History.objects.filter(username=username)
            for history in histories:
                if history.tag == '0':
                    movie_type['top250'] = movie_type.setdefault('top250', 0) + 1
                else:
                    movie = Movie.objects.get(id=history.video_id)
                    movie_type[movie.type] = movie_type.setdefault(movie.type, 0) + 1
            # 取出类型的前三种类型
            movie_number = 3
            while len(movie_type) != 0 and movie_number > 0:
                max_type = max(movie_type, key=movie_type.get)
                if max_type != 'top250':
                    movies.extend(Movie.objects.filter(type=max_type).order_by('-star')[0:movie_number])
                else:
                    movies.extend(DouBanMovie.objects.order_by('-star')[0:movie_number])
                del movie_type[max_type]
                movie_number = movie_number - 1
        else:
            flag = 1  # 用户推荐
            for item in recommend_list:
                movie = Movie.objects.filter(name=item[0])
                if len(movie) != 0:
                    movies.extend(movie)
                else:
                    movies.extend(DouBanMovie.objects.filter(name=item[0]))
        num = len(movies)
        return render(request, 'user/recommend_movie.html', {'user': user, 'movies': movies, 'num': num, 'flag': flag})
    else:
        messages.error(request, "请登录后再操作！")
        return redirect('/movie/index')


# 用户对电影进行评论
def comment_movie(request):
    data = {}
    comment_list = []
    username = request.session['username']
    user = User.objects.get(username=username)
    movie_id = request.GET.get('id')
    movie_type = request.GET.get('type')
    if movie_type == '豆瓣top250':
        tag = 0
        UserComment.objects.create(user=user, video_id=movie_id, comment=request.GET['comment'])
    else:
        tag = 1
        UserComment.objects.create(user=user, video_id=movie_id, comment=request.GET['comment'], tag=tag)
    comments = UserComment.objects.filter(Q(video_id=movie_id) & Q(tag=tag)).order_by('-ctime')[0:2]
    for comment in comments:
        comment_list.append([comment.user.username, comment.comment, comment.ctime.strftime("%Y-%m-%d %H:%M")])
    data['data'] = comment_list
    return JsonResponse(data, safe=False)




