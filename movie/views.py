from django.http import JsonResponse
from django.shortcuts import render
from movie.models import DouBanMovie, Movie
from user.models import History, UserComment
from django.core.paginator import Paginator
from django.utils import timezone
from django.db.models import Q


# Create your views here.


# index 显示主页
def index(request):
    movies = DouBanMovie.objects.order_by('?')[:25]
    latest_movies = Movie.objects.filter(classify='movie').filter(type='最新').order_by('?')[:12]
    hotting_movies = Movie.objects.filter(classify='movie').filter(type='热门').order_by('?')[:12]
    high_movies = Movie.objects.filter(classify='movie').filter(type='豆瓣高分').order_by('?')[:12]
    welcome1 = Movie.objects.filter(classify='movie').order_by('-star')[:6]
    welcome2 = Movie.objects.filter(classify='movie').order_by('-star')[6:12]
    welcome3 = Movie.objects.filter(classify='movie').order_by('-star')[12:18]
    # l = list(result)  # Queryset是惰性的，强制将Queryset转为list
    if 'username' in request.session.keys():
        username = request.session['username']
    else:
        username = None
    return render(request, 'movie/index.html',
                  {'username': username, "movies": movies, 'latest_movies': latest_movies,
                   'hotting_movies': hotting_movies, 'high_movies': high_movies,
                   'welcome1': welcome1, 'welcome2': welcome2, 'welcome3': welcome3})


# movie_detail 显示电影详情
def movie_detail(request, movie_id):
    current_time = timezone.now().strftime("%Y%m%d%H%M%S")  # 获取当前时间并格式化
    movies = DouBanMovie.objects.order_by('?')[:10]
    videos = DouBanMovie.objects.order_by('?')[:2]
    latest_movies = DouBanMovie.objects.order_by('?')[:6]
    if 'tag' in request.GET.keys():
        movie = Movie.objects.get(id=movie_id)
        tag = 1
    else:
        movie = DouBanMovie.objects.get(id=movie_id)
        tag = 0
    if 'username' in request.session.keys():
        username = request.session['username']
        History.objects.create(username=username, video_id=movie.id, current_time=current_time, tag=tag)
    else:
        username = None
    return render(request, 'movie/movie_detail.html',
                  {'username': username, "movie": movie, "movies": movies, "videos": videos,
                   "latest_movies": latest_movies})


# play_movie 播放界面
def play_movie(request):
    movies = DouBanMovie.objects.order_by('?')[:10]
    mt_type = request.GET.get('type')
    if 'username' in request.session.keys():
        username = request.session['username']
    else:
        username = None
    if mt_type == '豆瓣top250':
        tag = 0
        movie = DouBanMovie.objects.get(id=request.GET.get('id'))
        similarity_movies = DouBanMovie.objects.all().order_by('?')[0:6]
    else:
        tag = 1
        movie = Movie.objects.get(id=request.GET.get('id'))
        similarity_movies = Movie.objects.filter(type=mt_type).order_by('?')[0:6]
    comment_list = UserComment.objects.filter(Q(tag=tag) & Q(video_id=movie.id)).order_by('-ctime')[0:2]
    return render(request, 'movie/play_movie.html', {'username': username, "movies": movies,
                                                     'movie': movie, 'similarity_movies': similarity_movies,
                                                     'comment_list': comment_list})


# movie_type 电影类型列表
def movie_type(request, page):
    # 获取电影类型
    type = None
    if 'tag' in request.GET.keys():
        type = request.GET['tag']
    # 返回按钮效果
    result = 0
    if type == '华语' or type == '欧美' or type == '日本' or type == '韩国':
        result = 1
    # 得到该类型的所有电影
    all_movies = Movie.objects.filter(classify='movie').filter(type=type).order_by('-star')
    # 分页，按每页24条数据进行分页
    paginator = Paginator(all_movies, 24)
    # 获取第page页内容
    if page == '':
        # 默认取第一页的内容
        page = 1
    else:
        page = int(page)
    # movies是Page类的实例对象
    movies = paginator.page(page)
    if 'username' in request.session.keys():
        username = request.session['username']
    else:
        username = None
    recommend_movies = Movie.objects.filter(classify='movie').filter(type=type).order_by('?')[:9]
    return render(request, 'movie/movie_type.html',
                  {'username': username, 'type': type, 'movies': movies,
                   'pages': paginator.page_range, 'result': result, 'recommend_movies': recommend_movies})


def tv_type(request):
    # 得到该类型的所有电视
    hotting_tvs = Movie.objects.filter(classify='tv').filter(type='热门').order_by('?')[:12]
    domestic_tvs = Movie.objects.filter(classify='tv').filter(type='国产剧').order_by('?')[:12]
    england_tvs = Movie.objects.filter(classify='tv').filter(type='英剧').order_by('?')[:12]
    america_tvs = Movie.objects.filter(classify='tv').filter(type='美剧').order_by('?')[:12]
    japan_tvs = Movie.objects.filter(classify='tv').filter(type='日剧').order_by('?')[:12]
    japan_cartoon = Movie.objects.filter(classify='tv').filter(type='日本动画').order_by('?')[:12]
    korean_tvs = Movie.objects.filter(classify='tv').filter(type='韩剧').order_by('?')[:12]
    variety_tvs = Movie.objects.filter(classify='tv').filter(type='综艺').order_by('?')[:12]
    gang_tvs = Movie.objects.filter(classify='tv').filter(type='港剧').order_by('?')[:12]
    documentary = Movie.objects.filter(classify='tv').filter(type='纪录片').order_by('?')[:12]
    if 'username' in request.session.keys():
        username = request.session['username']
    else:
        username = None
    return render(request, 'movie/tv_type.html', {'username': username,
                                                  'tv1': hotting_tvs, 'tv2': domestic_tvs,
                                                  'tv3': england_tvs, 'tv4': america_tvs,
                                                  'tv5': japan_tvs, 'tv6': japan_cartoon,
                                                  'tv7': korean_tvs, 'tv8': variety_tvs,
                                                  'tv9': gang_tvs, 'tv10': documentary})


# 将迭代数据进行分组
def group(item, number):
    videos = []
    split = []
    for video in item:
        split.append(video)
        if len(split) == number:
            videos.append(split)
            split = []
    return videos


# new_publish 最新上映
def new_publish(request):
    new_movies = Movie.objects.filter(classify='movie').filter(pub_time='2020').order_by('?')[:16]
    new_tvs = Movie.objects.filter(classify='tv').filter(pub_time='2020').order_by('?')[:16]
    movies = group(new_movies, 2)
    tvs = group(new_tvs, 2)
    db_movie = DouBanMovie.objects.order_by('-star')[:10]
    if 'username' in request.session.keys():
        username = request.session['username']
    else:
        username = None
    return render(request, 'movie/new_publish.html', {'username': username,
                                                      'movies': movies, 'tvs': tvs, 'movie_list': db_movie})


# search_list 电影搜索列表
def search_list(request):
    if 'username' in request.session.keys():
        username = request.session['username']
    else:
        username = None
    return render(request, 'movie/search_list.html', {'username': username})


# search 获取查询后返回的数据
def search(request):
    data = {}
    name = request.GET['search']
    if name == 'star' or name == '-star' or name == 'evaluate_num' or name == '-evaluate_num':
        lists = Movie.objects.order_by(name).values()
    else:
        lists = Movie.objects.filter(name__contains=name).values()
    data['data'] = list(lists)
    return JsonResponse(data, safe=False)


# 访问页面找不到
def page_not_found(request, exception):
    return render(request, 'error/404.html')


# 内部服务器发生错误
def page_error(request):
    return render(request, 'error/500.html')
