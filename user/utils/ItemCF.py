from movie.models import DouBanMovie, Movie
from math import sqrt
import operator


# 1、构建用户->电影的倒排
def load_data(all_data):
    data = {}
    for history in all_data:
        data.setdefault(history.username, {})
        if history.tag == 0:
            movie = DouBanMovie.objects.get(id=history.video_id)
        else:
            movie = Movie.objects.get(id=history.video_id)
        data[history.username][movie.name] = history.evaluate_star
    return data


# 2、计算
# 2.1、构造电影->电影的共现矩阵
# 2.2、计算电影->电影的相似矩阵
def similarity(data):
    # 2.1、构造电影：电影的共现矩阵
    movie_i_count = {}     # 喜欢电影i的总人数
    movie_i_j = {}      # 喜欢电影i的也喜欢电影j的人数
    for username, movies in data.items():
        for movie_name_i, star in movies.items():
            movie_i_count.setdefault(movie_name_i, 0)
            movie_i_count[movie_name_i] += 1
            movie_i_j.setdefault(movie_name_i, {})
            for movie_name_j, star in movies.items():
                if movie_name_j not in movie_name_i:
                    movie_i_j[movie_name_i].setdefault(movie_name_j, 0)
                    movie_i_j[movie_name_i][movie_name_j] += 1
    # 2.2、计算电影与电影的相似矩阵
    similarity_i_j = {}     # 电影i与j的相似矩阵
    for movie_i_name, data in movie_i_j.items():
        similarity_i_j.setdefault(movie_i_name, {})
        for movie_j_name, movies in data.items():
            similarity_i_j[movie_i_name].setdefault(movie_j_name, 0)
            similarity_i_j[movie_i_name][movie_j_name] =\
                movie_i_j[movie_i_name][movie_j_name] / sqrt(movie_i_count[movie_i_name] * movie_i_count[movie_j_name])
    return similarity_i_j


# 3、根据用户的历史记录，给用户推荐电影
# key=operator.itemgetter(1) 在sorted中表明按数据的第二个域进行排序，此处即按相似度排序
def recommend_list(data, similarity_i_j, user, k=3, n=10):
    rank = {}   # 推荐的电影集合
    # 当用户有评分记录时返回相应的推荐集合，没有评分记录则返回[]
    try:
        for movie_name, star in data[user].items():     # 获取用户的评分记录
            for movie, similarity in sorted(similarity_i_j[movie_name].items(), key=operator.itemgetter(1), reverse=True)[0:k]:
                if movie not in data[user].keys():  # 该相似的电影不在用户的观看记录中
                    rank.setdefault(movie, 0)
                    # 预测兴趣度 = 本电影的评分 * 本电影和其它电影的相似度
                    rank[movie] += float(star) * similarity
        return sorted(rank.items(), key=operator.itemgetter(1), reverse=True)[0:n]
    except:
        return []


# 执行以上步骤，获取推荐列表
def get_recommend(data, user):
    format_data = load_data(data)
    similarity_i_j = similarity(format_data)
    rank = recommend_list(format_data, similarity_i_j, user)
    return rank







