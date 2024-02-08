from django.shortcuts import render,redirect
from .models import *

from .forms import ArticleForm
from django.contrib.auth.decorators import login_required

from django.views.generic.edit import UpdateView,DeleteView
from django.urls import reverse_lazy
from django.core.paginator import Paginator

# Create your views here.

def categories(request):
    categories = Category.objects.all()

    return {
        'categories' : categories,
    }

def search_article(request):
    if 'query' in request.GET:
        query=request.GET['query']
        articles=Article.objects.filter(title__icontains=query) | Article.objects.filter(content__icontains=query)
        context={
            'articles':articles,
            'query':query
        }
    return render(request,'article/categorised_article.html',context)

def index(request):
    all_articles=Article.objects.all()[::-1]
    paginator=Paginator(all_articles,4)
    page_num=request.GET.get('page')
    page_obj=paginator.get_page(page_num)
    recent_articles=Article.objects.all().order_by('-date')[:3]
    context={
        # 'articles':all_articles,
        'page_obj':page_obj,
        'recent_articles':recent_articles
    }
    return render(request,'article/index.html',context)

def single_article(request,pk):
    article=Article.objects.get(pk=pk)
    comments=Comment.objects.filter(article=article)
    if request.method=='POST':
        if 'delete-comment' in request.POST:
            id = request.POST.get('delete-comment')
            comment = Comment.objects.get(pk=id)
            comment.delete()
            return redirect('article:single_article', pk=article.pk)
        else:
            comment=request.POST.get('comment')
            user=request.user
            new_comment=Comment(text=comment,user=user,article=article)
            new_comment.save()
            return redirect('article:single_article', pk=article.pk)
    context ={
        "article":article,
        "comments":comments[::-1],
    }
    return render(request, 'article/article.html',context)

def categorised_article(request,pk):
    if pk!=0:
        category=Category.objects.get(pk=pk)
        articles=Article.objects.filter(category=category).all()
    else:
        articles=Article.objects.all()
        category="All"
    context={
        'articles':articles,
        'category':category
    }
    return render(request,'article/categorised_article.html',context)

@login_required
def create_article(request):

    form = ArticleForm()

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES) 
        if form.is_valid():
            article=form.save(commit=False)
            article.author=request.user
            article.save()
            return redirect('article:index')

    context = {
        "form" : form,
    }

    return render(request, 'article/article_form.html', context) 
  

class UpdateArticle(UpdateView):
    model =Article
    # fields= ["category","title","img","content"]
    form_class=ArticleForm
    template_name_suffix="_update"

class DeleteArticle(DeleteView):
    model= Article
    success_url=reverse_lazy('profile')