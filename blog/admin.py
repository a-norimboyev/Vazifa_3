from django.contrib import admin
from .models import Category, Tag, Post, Comment

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.action(description="Tanlangan postlarni tasdiqlash (Asosiy sahifada ko'rinadi)")
def approve_posts(modeladmin, request, queryset):
    updated = queryset.update(is_approved=True)
    modeladmin.message_user(request, f"{updated} ta post muvaffaqiyatli tasdiqlandi.")


@admin.action(description="Tanlangan postlar tasdig'ini bekor qilish")
def unapprove_posts(modeladmin, request, queryset):
    updated = queryset.update(is_approved=False)
    modeladmin.message_user(request, f"{updated} ta post tasdig'i bekor qilindi.")


@admin.action(description="Tanlangan postlarni Tavsiya etilgan deb belgilash")
def make_recommended(modeladmin, request, queryset):
    updated = queryset.update(is_recommended=True)
    modeladmin.message_user(request, f"{updated} ta post tavsiya etilgan deb belgilandi.")


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "category", "is_approved", "is_recommended", "views_count", "created_at")
    list_filter = ("is_approved", "is_recommended", "category", "created_at")
    search_fields = ("title", "content", "author__username")
    list_editable = ("is_approved", "is_recommended")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("tags",)
    actions = [approve_posts, unapprove_posts, make_recommended]
    date_hierarchy = "created_at"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("author", "post", "created_at")
    list_filter = ("created_at",)
    search_fields = ("content", "author__username", "post__title")
