from faker import Faker
from .models import BlogPost

fake = Faker()

def create_blog_posts(n):
    blog_posts = []
    for _ in range(n):
        title = fake.sentence(nb_words=6)
        content = fake.text(max_nb_chars=2000)

        blog_post = BlogPost(title=title, content=content)
        blog_posts.append(blog_post)

    BlogPost.objects.bulk_create(blog_posts)

create_blog_posts(100)
