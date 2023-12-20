from ..translatable_model_serializer import TranslatableModelSerializer
from ..models import BlogPost


class BlogPostSerializer(TranslatableModelSerializer):
    class Meta:
        model = BlogPost
        fields = ["id", "pk", "title", "content", "published_date", "updated_date"]
        translated_fields = ["title", "content", "random"]

    def get_random(self, obj):
        return "random"
