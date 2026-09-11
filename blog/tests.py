from django.test import TestCase
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from blog.models import Post, Category, Tag, Comment

# Create your tests here.

class BlogPlatformTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.admin_user = User.objects.create_superuser(username="adminuser", password="adminpassword123")
        self.category = Category.objects.create(name="Texnologiya")
        self.tag = Tag.objects.create(name="django")

        # 1x1 piksel o'lchamdagi kichik test rasm (GIF)
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        self.test_image = SimpleUploadedFile("test.gif", small_gif, content_type="image/gif")

        # Tasdiqlangan post
        self.approved_post = Post.objects.create(
            title="Tasdiqlangan Maqola",
            author=self.user,
            category=self.category,
            content="Bu hamma uchun ochiq maqola.",
            image=self.test_image,
            is_approved=True,
            is_recommended=True,
            views_count=10
        )
        self.approved_post.tags.add(self.tag)

        # Tasdiqlanmagan post
        self.unapproved_post = Post.objects.create(
            title="Tasdiqlanmagan Maqola",
            author=self.user,
            category=self.category,
            content="Bu faqat muallif va adminga ko'rinishi kerak.",
            image=self.test_image,
            is_approved=False,
            is_recommended=False,
            views_count=0
        )

    def test_home_page_only_shows_approved_posts(self):
        """Asosiy sahifada faqat tasdiqlangan postlar chiqishi kerak"""
        response = self.client.get(reverse("blog:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.approved_post.title)
        self.assertNotContains(response, self.unapproved_post.title)

    def test_home_page_tabs(self):
        """Asosiy sahifadagi barcha filtr tablari to'g'ri ishlashi kerak"""
        for tab in ["latest", "most_viewed", "weekly", "monthly", "recommended"]:
            response = self.client.get(reverse("blog:home"), {"tab": tab})
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, self.approved_post.title)

    def test_post_detail_view_count(self):
        """Postga kirilganda ko'rishlar soni oshishi kerak"""
        initial_views = self.approved_post.views_count
        response = self.client.get(reverse("blog:post_detail", kwargs={"slug": self.approved_post.slug}))
        self.assertEqual(response.status_code, 200)
        self.approved_post.refresh_from_db()
        self.assertEqual(self.approved_post.views_count, initial_views + 1)

    def test_unapproved_post_access_denied_to_anonymous(self):
        """Oddiy tashrif buyuruvchi tasdiqlanmagan postni ko'ra olmasligi kerak (404)"""
        response = self.client.get(reverse("blog:post_detail", kwargs={"slug": self.unapproved_post.slug}))
        self.assertEqual(response.status_code, 404)

    def test_unapproved_post_access_allowed_to_author(self):
        """Post muallifi o'zining tasdiqlanmagan postini ko'ra olishi kerak"""
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse("blog:post_detail", kwargs={"slug": self.unapproved_post.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Kutilmoqda")

    def test_create_post_by_user_is_unapproved_by_default(self):
        """Foydalanuvchi yangi post qo'shganda is_approved=False bo'lishi kerak"""
        self.client.login(username="testuser", password="password123")
        gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        img = SimpleUploadedFile("new_post.gif", gif, content_type="image/gif")
        response = self.client.post(reverse("blog:post_create"), {
            "title": "Foydalanuvchining yangi posti",
            "category": self.category.id,
            "image": img,
            "content": "Yangi postning to'liq matni",
            "new_tags": "test, yangilik"
        })
        self.assertEqual(response.status_code, 302) # redirect to my_posts
        new_post = Post.objects.get(title="Foydalanuvchining yangi posti")
        self.assertFalse(new_post.is_approved)
        self.assertEqual(new_post.author, self.user)

    def test_comment_submission(self):
        """Kirgan foydalanuvchi izoh qoldira olishi kerak"""
        self.client.login(username="testuser", password="password123")
        response = self.client.post(
            reverse("blog:post_detail", kwargs={"slug": self.approved_post.slug}),
            {"content": "Ajoyib maqola, rahmat!"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Comment.objects.filter(post=self.approved_post, content="Ajoyib maqola, rahmat!").exists())
