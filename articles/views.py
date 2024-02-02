from django.shortcuts import render, redirect, get_object_or_404
from .models import Article, Author


def index(request):
    context = Article.objects.all().order_by('name')
    return render(request, 'articles/articles.html', {'context': context})


def articles_id(request, article_id):
    context = get_object_or_404(Article, id=article_id)
    return render(request, 'articles/articles_id.html', {'context': context})


def author_detail(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    articles = Article.objects.filter(author=author)
    return render(request, 'articles/authors_detail.html', {'author': author, 'articles': articles})


def like(request):
    id_article = request.POST['id_article']
    context = Article.objects.get(id=id_article)
    context.like_count += 1
    context.save()
    return redirect('articles:articles_id', context.id)
