from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from .models import BlogPost
from tms.forms.post_blog import BlogPostForm
from .serializers.blog_post import BlogPostSerializer
from .translated import translated


@translated(owner="i18n")
def post_list(request):
    posts = BlogPost.objects.all()
    return render(
        request,
        "blog/post_list.html",
        {"posts": BlogPostSerializer(posts, many=True).data},
    )


@translated(owner="i18n")
def post_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    return render(
        request, "blog/post_detail.html", {"post": BlogPostSerializer(post).data}
    )


def post_new(request):
    if request.method == "POST":
        form = BlogPostForm(request.POST)
        if form.is_valid():
            post = form.save()
            return redirect("post_detail", pk=post.pk)
    else:
        form = BlogPostForm()
    return render(request, "blog/post_edit.html", {"form": form})


def post_edit(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == "POST":
        form = BlogPostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save()
            return redirect("post_detail", pk=post.pk)
    else:
        form = BlogPostForm(instance=post)
    return render(request, "blog/post_edit.html", {"form": form})
