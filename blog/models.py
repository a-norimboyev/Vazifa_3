from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse
import uuid

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Kategoriya nomi")
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name) or "category"
            slug = base_slug
            counter = 1
            while Category.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("blog:category_posts", kwargs={"slug": self.slug})


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Teg nomi")
    slug = models.SlugField(max_length=60, unique=True, blank=True)

    class Meta:
        verbose_name = "Teg"
        verbose_name_plural = "Teglar"
        ordering = ["name"]

    def __str__(self):
        return f"#{self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name) or "tag"
            slug = base_slug
            counter = 1
            while Tag.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("blog:tag_posts", kwargs={"slug": self.slug})


class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name="Sarlavha")
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts", verbose_name="Muallif")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="posts", verbose_name="Bo'lim")
    tags = models.ManyToManyField(Tag, related_name="posts", blank=True, verbose_name="Teglar")
    image = models.ImageField(upload_to="posts/%Y/%m/", verbose_name="Rasm")
    image = models.ImageField(upload_to="posts/%Y/%m/", verbose_name="Rasm", blank=True, null=True)
    content = models.TextField(verbose_name="Post matni")
    
    # Statistika va Holat
    views_count = models.PositiveIntegerField(default=0, verbose_name="Ko'rishlar soni")
    is_approved = models.BooleanField(default=False, verbose_name="Admin tomonidan tasdiqlangan")
    is_recommended = models.BooleanField(default=False, verbose_name="Tavsiya etilgan post")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan sana")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan sana")

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Postlar"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title) or f"post-{uuid.uuid4().hex[:6]}"
            slug = base_slug
            counter = 1
            while Post.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("blog:post_detail", kwargs={"slug": self.slug})


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments", verbose_name="Post")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments", verbose_name="Foydalanuvchi")
    content = models.TextField(verbose_name="Izoh matni")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yozilgan sana")

    class Meta:
        verbose_name = "Izoh"
        verbose_name_plural = "Izohlar"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.author.username} - {self.post.title[:30]}"
