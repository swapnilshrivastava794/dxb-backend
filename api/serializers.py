from rest_framework import serializers
from django.utils import timezone
from post_management.models import (
    NewsPost, Journalist, category, sub_category, VideoNews
)


class NewsPostSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    posted_by = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()

    class Meta:
        model = NewsPost
        fields = [
            "id",
            "post_title",
            "meta_title",
            "slug",
            "post_short_des",
            "image",
            "category",
            "posted_by",
            "post_date",
            "schedule_date",
            "viewcounter",
            "status",
            "trending",
            "Head_Lines",
            "BreakingNews",
            "articles",
            "Event",
            "tags"
        ]

    # -----------------------------
    # Category
    # -----------------------------
    def get_category(self, obj):
        if obj.post_cat:
            return {
                "id": obj.post_cat.id,
                "name": getattr(obj.post_cat, "sub_cat_name", None),
                "slug": getattr(obj.post_cat, "slug", None)
            }
        return None

    # -----------------------------
    # Posted By (journalist/author)
    # -----------------------------
    def get_posted_by(self, obj):
        if obj.journalist:
            return {
                "type": "journalist",
                "id": obj.journalist.id,
                "username": obj.journalist.username
            }
        if obj.author:
            return {
                "type": "author",
                "id": obj.author.id,
                "username": obj.author.username
            }
        return None

    # -----------------------------
    # Image URL
    # -----------------------------
    def get_image(self, obj):
        request = self.context.get("request")
        if obj.post_image:
            if request:
                return request.build_absolute_uri(obj.post_image.url)
            return obj.post_image.url
        return None

    # -----------------------------
    # ManyToMany Tags
    # -----------------------------
    def get_tags(self, obj):
        return [
            {
                "id": tag.id,
                "name": tag.name,
                "slug": getattr(tag, "slug", None)
            }
            for tag in obj.tags.all()
        ]


class JournalistListSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField()

    class Meta:
        model = Journalist
        fields = [
            "id",
            "username",
            "email",
            "profile_image",
        ]

    def get_profile_image(self, obj):
        request = self.context.get("request")
        if hasattr(obj, "profile_image") and obj.profile_image:
            if request:
                return request.build_absolute_uri(obj.profile_image.url)
            return obj.profile_image.url
        return None
    
    
class VideoNewsSerializer(serializers.ModelSerializer):
    thumbnail = serializers.SerializerMethodField()
    
    class Meta:
        model = VideoNews
        fields = [
            "id",
            "video_title",
            "slug",
            "video_short_des",
            "thumbnail",
            "video_url",
            "video_type",
            "order",
            "schedule_date",
            "video_date",
        ]

    def get_thumbnail(self, obj):
        request = self.context.get("request")
        if obj.video_thumbnail:
            if request:
                return request.build_absolute_uri(obj.video_thumbnail.url)
            return obj.video_thumbnail.url
        return None


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = sub_category
        fields = [
            "id",
            "subcat_name",
            "subcat_slug",
            "order",
        ]


class CategoryListSerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = category
        fields = [
            "id",
            "cat_name",
            "cat_slug",
            "order",
            "subcategories",
        ]

    def get_subcategories(self, obj):
        subcats = obj.sub_category_set.filter(
            subcat_status='active'
        ).order_by("order")

        return SubCategorySerializer(subcats, many=True).data
