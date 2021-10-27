from django import template     # 导入有模板语法的包
register = template.Library()   # 必须创建这个实例对象


# 创建一个template能认识的函数
# 自定义一个过滤器函数    {{  }}
# filter只能加一个参数
@register.filter
def format_date(date):
    return date[0:4] + '-' + date[4:6] + '-' + date[6:8] + ' ' + date[8:10] + ':' + date[10:12] + ':' + date[12:14]


# 自定义一个过滤器      {%  %}
@register.simple_tag
def multi(x, y, z):
    return x * y *z
