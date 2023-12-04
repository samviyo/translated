from django.shortcuts import render
from django.core.paginator import Paginator
from .models import BlogPost
from .serializers.blog_post import BlogPostSerializer
from .translated import translated, lazy_translate as _


def get_blog_posts(page=1):
    posts_list = BlogPost.objects.order_by("id")
    paginator = Paginator(posts_list, 10)
    serializer = BlogPostSerializer(paginator.page(page), many=True)

    return serializer.data


@translated(owner="AppSec")
def index(request):
    page = request.GET.get("page", 1)
    return render(
        request,
        "index.html",
        {
            "blog_posts": get_blog_posts(page),
            "random": f"Hello, {_('world')}. You're at the {_('tms')} index.",
        },
    )
