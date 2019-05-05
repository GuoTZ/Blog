from django import template

from blog_app.models import Article, Category,Tag

register = template.Library()


@register.simple_tag
def get_months_num(num=0):
    if num==0:
        list =  Article.objects.datetimes('pub_time', 'month', order='DESC')
    else:
        list =  Article.objects.datetimes('pub_time', 'month', order='DESC')[0:10]
    return list 

@register.simple_tag
def get_tags_num(num=0):
    if num==0:
        list = Tag.objects.all()
    else:
        list = Tag.objects.all()[0:10] 
    return list  # 获取全部的标签对象

@register.simple_tag
def get_cate_num(num=0):
    print(num)
    if num==0:
        list = Category.objects.all()
    else:
        list = Category.objects.all()[0:10]
    return list  # 获取全部的分类对象
