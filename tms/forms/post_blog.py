from django import forms
from tms.models import BlogPost


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ("title", "content")
