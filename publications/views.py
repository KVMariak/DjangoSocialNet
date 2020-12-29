from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.http import HttpResponse
from .models import Post
from .forms import CreatePostForm, UpdatePostForm
from profiles.models import User


def create_post_view(request):
    context = {}

    user = request.user
    if not user.is_authenticated:
        return redirect('must_authenticate')

    form = CreatePostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        author = User.objects.filter(email=user.email).first()
        obj.author = author
        obj.save()
        form = CreatePostForm()
        return redirect('home')

    context['form'] = form

    return render(request, "publications/create_publication.html", context)


def detail_post_view(request, slug):
    context = {}

    blog_post = get_object_or_404(Post, slug=slug)
    context['blog_post'] = blog_post

    return render(request, 'blog/detail_blog.html', context)


def edit_post_view(request, slug):
    context = {}

    user = request.user
    if not user.is_authenticated:
        return redirect("must_authenticate")

    blog_post = get_object_or_404(Post, slug=slug)

    if blog_post.author != user:
        return HttpResponse("You are not the author of that post.")

    if request.POST:
        form = UpdatePostForm(request.POST or None, request.FILES or None, instance=blog_post)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            context['success_message'] = "Updated"
            blog_post = obj

    form = UpdatePostForm(
        initial={
            "title": blog_post.title,
            "body": blog_post.body,
            "image": blog_post.image,
        }
    )

    context['form'] = form
    return render(request, 'blog/edit_blog.html', context)


def get_post_queryset(query=None):
    queryset = []
    queries = query.split(" ")
    for q in queries:
        posts = Post.objects.filter(
            Q(title__icontains=q) |
            Q(body__icontains=q)
        ).distinct()

        for post in posts:
            queryset.append(post)

    return list(set(queryset))
