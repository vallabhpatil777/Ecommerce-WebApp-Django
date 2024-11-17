from typing import Any
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Post, Category, Comment
from .forms import PostForm, EditForm, CommentForm

from hitcount.views import HitCountDetailView
from django.contrib import messages

import time


class BlogView(ListView):
    paginate_by = 4
    model = Post
    template_name = 'blog.html'
    ordering = ['-date_created',]
    
    
    
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        cat_menu = Category.objects.all()
        context = super(BlogView, self).get_context_data(**kwargs)
        context["cat_menu"] = cat_menu
        return context
    
class BlogDetailView(HitCountDetailView):
    model = Post
    template_name = 'article_dateils.html'
    count_hit = True
    
    form = CommentForm
    
    def post(self, request, pk, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            post = self.get_object()
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            
            return redirect(reverse('blog_detail', args=[str(pk)]))
        
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super(BlogDetailView, self).get_context_data(**kwargs)
        stuff = get_object_or_404(Post, id = self.kwargs['pk'])
        total_likes = stuff.total_likes()
        stuff.visit = stuff.visit + 1
        
        
        post_comments = Comment.objects.filter(post=self.object.id)
        comment_count = post_comments.count()
        
        
        liked = False
        if stuff.like.filter(id=self.request.user.id).exists():
            liked = True
        
        context["total_likes"] = total_likes
        context["liked"] = liked
        context["form"] = self.form
        context["post_comments"] = post_comments
        context["comment_count"] = comment_count
        stuff.save()
        return context

    
def add_post(request):
    context = {}
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data.get("title")
            body = form.cleaned_data.get("body")
            snippet = form.cleaned_data.get("snippet")
            category = form.cleaned_data.get("category")
            image = form.cleaned_data.get("image")
            author = request.user
            
            obj = Post.objects.create(
                                 title = title, 
                                 author = author,
                                 body = body,
                                 snippet = snippet,
                                 category = category,
                                 image = image
                                 
                                 )
            obj.save()
            return redirect('blog')
    else:
        form = PostForm()
    context['form']= form
    return render(request, "add_post.html", context)
    

class EditPostView(UpdateView):
    model = Post
    template_name = 'edit_post.html'
    form_class = EditForm
    

class DeletePostView(DeleteView):
    model = Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy('blog')
    
    
def CategoryView(request, cat):
    
    cat = cat.replace('-', ' ')
    
    try:
        category = Category.objects.get(name=cat)
        posts = Post.objects.filter(category=category)
        return render(request, 'blog_categories.html', {'posts': posts, 'category': category})
    except:
        
        return redirect('blog')
def category_view(request, cat):
    
    cat = cat.replace('-', ' ')
    print('ok')
    try:
        
		# Look Up The Category
        category = Category.objects.get(name=cat)
        print('still ok')
        posts = Post.objects.filter(category=category)
        print('nice')
        return render(request, 'blog_categories.html', {'posts':posts, 'category':category})
    except:
        print('not ok')
        messages.success(request, ("همچین دسته بندی وجود ندارد..."))
        return redirect('blog')


def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    liked = False
    if post.like.filter(id=request.user.id).exists():
        post.like.remove(request.user)
        liked = False
    else:
        post.like.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('blog_detail', args=[str(pk)]))


def VisitView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    
    post.visit.add(request.user)
    
    return HttpResponseRedirect(reverse('blog', args=[str(pk)]))


def search_blog(request):
    if request.method == 'POST':
        postsearched = request.POST.get('postsearched')
        posts = Post.objects.filter(title__contains=postsearched)
        
    return render(request, 'search_blog.html', {'postsearched': postsearched, 'posts': posts})

    
    