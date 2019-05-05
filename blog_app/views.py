from django.shortcuts import render
from blog_app.models import Article, Category,Tag
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404,HttpResponse
from django.conf import settings
import markdown
from django.db.models import Q
import json
# Create your views here.
def home(request):  # 主页
    posts = Article.objects.filter(status='p', pub_time__isnull=False)[0:20]
        
    for post in posts:
            # 记得在顶部引入 markdown 模块
        post.content = markdown.markdown(post.content,
                                    extensions=[
                                        'markdown.extensions.extra',
                                        'markdown.extensions.codehilite',
                                        'markdown.extensions.toc',
                                    ])
    return render(request, 'home.html', {'post_list': posts})

# Create your views here.
def mroe(request):  # 主页
    posts = Article.objects.filter(status='p', pub_time__isnull=False)  # 获取全部(状态为已发布，发布时间不为空)Article对象
    paginator = Paginator(posts, settings.PAGE_NUM)  # 每页显示数量
    page = request.GET.get('page')  # 获取URL中page参数的值
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
        
    for post in post_list:
            # 记得在顶部引入 markdown 模块
        post.content = markdown.markdown(post.content,
                                    extensions=[
                                        'markdown.extensions.extra',
                                        'markdown.extensions.codehilite',
                                        'markdown.extensions.toc',
                                    ])
    return render(request, 'mroe.html', {'post_list': post_list})

def detail(request, id):
    try:
        post = Article.objects.get(id=str(id))
        post.viewed()  # 更新浏览次数
        tags = post.tags.all()
        next_post = post.next_article()  # 上一篇文章对象
        prev_post = post.prev_article()  # 下一篇文章对象
        post.content = markdown.markdown(post.content,
                                    extensions=[
                                        'markdown.extensions.extra',
                                        'markdown.extensions.codehilite',
                                        'markdown.extensions.toc',
                                    ])
    except Article.DoesNotExist:
        raise Http404
    return render(
        request, 'post.html',
        {
            'post': post,
            'tags': tags,
            'next_post': next_post,
            'prev_post': prev_post,
        }
    )


def search_category(request, id):
    posts = Article.objects.filter(category_id=str(id))
    category = Category.objects.get(id=str(id))
    paginator = Paginator(posts, settings.PAGE_NUM)  # 每页显示数量
    try:
        page = request.GET.get('page')  # 获取URL中page参数的值
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)

    for post in post_list:
            # 记得在顶部引入 markdown 模块
        post.content = markdown.markdown(post.content,
                                    extensions=[
                                        'markdown.extensions.extra',
                                        'markdown.extensions.codehilite',
                                        'markdown.extensions.toc',
                                    ])
    return render(request, 'category.html',
                  {'post_list': post_list,
                   'category': category
                  }
    )


def search_tag(request, tag):
    posts = Article.objects.filter(tags__name__contains=tag)
    paginator = Paginator(posts, settings.PAGE_NUM)  # 每页显示数量
    try:
        page = request.GET.get('page')  # 获取URL中page参数的值
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return render(request, 'tag.html', {
        'post_list': post_list,
        'tag': tag
        }
    )
def search_key(request):
    key = request.POST.get('key')
    posts = Article.objects.filter(Q(title__icontains=key) | Q(tags__name__icontains=key) | Q(content__icontains=key))
    paginator = Paginator(posts, settings.PAGE_NUM)  # 每页显示数量
    try:
        page = request.GET.get('page')  # 获取URL中page参数的值
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return render(request, 'searchkey.html', {
        'post_list': post_list,
        'key': key
        }
    )


def archives(request, year, month):
    posts = Article.objects.filter(pub_time__year=year, pub_time__month=month).order_by('-pub_time')
    paginator = Paginator(posts, settings.PAGE_NUM)  # 每页显示数量
    try:
        page = request.GET.get('page')  # 获取URL中page参数的值
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return render(request, 'archive.html', {
        'post_list': post_list,
        'year_month': year+'年'+month+'月'
        }
    )

def formatJson(request):
    return render(request, 'formatJson.html',{'jsonStr':'','json_dicts':''})

def jsonFrom(request):
    jsonStr = request.POST.get('jsonStr')
    
    try:
        json_dicts=json.loads(jsonStr)
        js = json.dumps(json_dicts, sort_keys=True, indent=4, separators=(',', ':'),ensure_ascii=False)
        return render(request, 'formatJson.html',{'jsonStr':jsonStr,'json_dicts':js})
    except ValueError as e:
        return render(request, 'formatJson.html',{'jsonStr':jsonStr,'json_dicts':e})
    