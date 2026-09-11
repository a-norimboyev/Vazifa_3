import os
import django
from datetime import timedelta
from django.utils import timezone
from PIL import Image, ImageDraw, ImageFont
import io
from django.core.files.base import ContentFile

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog_project.settings")
django.setup()

from django.contrib.auth.models import User
from blog.models import Category, Tag, Post, Comment

def create_sample_image(text, color):
    img = Image.new("RGB", (800, 450), color=color)
    draw = ImageDraw.Draw(img)
    # Simple rectangle and circle decoration
    draw.rectangle([20, 20, 780, 430], outline="white", width=4)
    # Text placeholder in center (using default bitmap font or simple text)
    draw.text((50, 210), text, fill="white")
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG")
    return ContentFile(buffer.getvalue())

def seed():
    print("Test foydalanuvchilar yaratilmoqda...")
    # Admin
    admin, created = User.objects.get_or_create(username="admin", defaults={"email": "admin@example.com", "is_staff": True, "is_superuser": True})
    if created:
        admin.set_password("admin123")
        admin.save()
        print("Superuser: admin / admin123")

    # Regular users
    user1, _ = User.objects.get_or_create(username="javohir", defaults={"email": "javohir@example.com", "first_name": "Javohir", "last_name": "Karimov"})
    user1.set_password("testpass123")
    user1.save()

    user2, _ = User.objects.get_or_create(username="nodira", defaults={"email": "nodira@example.com", "first_name": "Nodira", "last_name": "Alimova"})
    user2.set_password("testpass123")
    user2.save()

    print("Kategoriyalar yaratilmoqda...")
    categories_data = [
        "Dasturlash",
        "Sun'iy Intellekt",
        "Kiberxavfsizlik",
        "Dizayn va UX"
    ]
    categories = {}
    for cat_name in categories_data:
        cat, _ = Category.objects.get_or_create(name=cat_name)
        categories[cat_name] = cat

    print("Teglar yaratilmoqda...")
    tags_data = ["python", "django", "web", "ai", "security", "design", "javascript", "backend"]
    tags = {}
    for t_name in tags_data:
        tag, _ = Tag.objects.get_or_create(name=t_name)
        tags[t_name] = tag

    print("Postlar yaratilmoqda...")
    now = timezone.now()

    posts_data = [
        {
            "title": "Django 5 da zamonaviy veb ilovalar yaratish",
            "author": admin,
            "category": categories["Dasturlash"],
            "tags": [tags["python"], tags["django"], tags["web"]],
            "content": "Django - bu Python dasturlash tilidagi eng kuchli va mashhur veb freymvorklardan biri. U 'batteries included' falsafasiga asoslangan bo'lib, o'z ichida autentifikatsiya, ma'muriyat paneli, ORM va kiberxavfsizlik himoyasini jamlagan.\n\nUshbu maqolada biz Django freymvorkining afzalliklari, model-view-template arxitekturasi va real loyihalarda qo'llanilishi haqida so'z yuritamiz.",
            "views_count": 345,
            "is_approved": True,
            "is_recommended": True,
            "color": (41, 128, 185),
            "days_ago": 2,
        },
        {
            "title": "Sun'iy intellekt 2026-yilda: Katta til modellari va kelajak",
            "author": user2,
            "category": categories["Sun'iy Intellekt"],
            "tags": [tags["ai"], tags["python"]],
            "content": "Sun'iy intellekt va neyron tarmoqlar bugungi kunda barcha sohalarga shiddat bilan kirib bormoqda. Matn yaratish, dastur kodlarini tahlil qilish va tasvirlarni generatsiya qilish imkoniyatlari kundan-kunga takomillashmoqda.\n\nKelgusi yillarda multimodal modellar inson faoliyatini yanada yengillashtirishga xizmat qilishi kutilmoqda.",
            "views_count": 820,
            "is_approved": True,
            "is_recommended": True,
            "color": (142, 68, 173),
            "days_ago": 4,
        },
        {
            "title": "Veb xavfsizlik: SQL Injection va XSS hujumlaridan himoyalanish",
            "author": user1,
            "category": categories["Kiberxavfsizlik"],
            "tags": [tags["security"], tags["web"]],
            "content": "Har qanday veb saytni yaratishda xavfsizlik birinchi o'rinda turishi kerak. Foydalanuvchi ma'lumotlarini tekshirish (validation), parollarni xesh qilish va CSRF tokenlaridan foydalanish saytni turli hujumlardan himoya qiladi.\n\nDjango freymvorki standart holatda SQL injection va XSS hujumlariga qarshi mustahkam himoyaga ega.",
            "views_count": 510,
            "is_approved": True,
            "is_recommended": False,
            "color": (192, 57, 43),
            "days_ago": 12,
        },
        {
            "title": "Zamonaviy UI/UX dizayn qoidalari: Foydalanuvchi uchun qulaylik",
            "author": user2,
            "category": categories["Dizayn va UX"],
            "tags": [tags["design"], tags["web"]],
            "content": "Interfeys dizayni nafaqat chiroyli ko'rinishi, balki tushunarli va qulay bo'lishi shart. Kontrast ranglar, to'g'ri tipografika va intuitiv navigatsiya foydalanuvchilarning saytdagi tajribasini yaxshilaydi.",
            "views_count": 180,
            "is_approved": True,
            "is_recommended": False,
            "color": (39, 174, 96),
            "days_ago": 18,
        },
        {
            "title": "PostgreSQL va Django: Katta hajmdagi ma'lumotlar bilan ishlash",
            "author": admin,
            "category": categories["Dasturlash"],
            "tags": [tags["python"], tags["backend"]],
            "content": "Ishlab chiqarish (production) muhitida PostgreSQL eng ishonchli va kuchli relyatsion ma'lumotlar bazasi hisoblanadi. Indekslar, tranzaksiyalar va optimallashtirish usullari bo'yicha amaliy maslahatlar.",
            "views_count": 95,
            "is_approved": True,
            "is_recommended": False,
            "color": (52, 73, 94),
            "days_ago": 1,
        },
        # TASDIQLANMAGAN POST (Admin approval tekshirish uchun)
        {
            "title": "Yangi boshlovchilar uchun Python asoslari (Kutilmoqda)",
            "author": user1,
            "category": categories["Dasturlash"],
            "tags": [tags["python"]],
            "content": "Ushbu post oddiy foydalanuvchi tomonidan kiritilgan bo'lib, hali admin tasdig'idan o'tmagan. Shu sababli bu post bosh sahifada ko'rinmaydi, faqat muallifning 'Mening postlarim' sahifasida va admin panelida ko'rinadi.",
            "views_count": 10,
            "is_approved": False,
            "is_recommended": False,
            "color": (230, 126, 34),
            "days_ago": 0,
        },
    ]

    for p_info in posts_data:
        post, p_created = Post.objects.get_or_create(
            title=p_info["title"],
            defaults={
                "author": p_info["author"],
                "category": p_info["category"],
                "content": p_info["content"],
                "views_count": p_info["views_count"],
                "is_approved": p_info["is_approved"],
                "is_recommended": p_info["is_recommended"],
            }
        )
        if p_created:
            # Vaqtini sozlash
            post.created_at = now - timedelta(days=p_info["days_ago"])
            # Rasm yaratish
            img_file = create_sample_image(p_info["title"][:25], p_info["color"])
            post.image.save(f"post_{post.id}.jpg", img_file, save=False)
            post.save()
            post.tags.set(p_info["tags"])
            print(f"Post yaratildi: {post.title} (Tasdiqlangan: {post.is_approved})")

    # Izohlar
    first_post = Post.objects.filter(is_approved=True).first()
    if first_post:
        Comment.objects.get_or_create(
            post=first_post,
            author=user1,
            defaults={"content": "Juda foydali va qiziqarli maqola bo'libdi, rahmat!"}
        )
        Comment.objects.get_or_create(
            post=first_post,
            author=user2,
            defaults={"content": "Django bilan ishlash bo'yicha yana ko'proq postlar kutamiz!"}
        )
        print("Izohlar qo'shildi.")

    print("\nBoshlang'ich ma'lumotlar muvaffaqiyatli yuklandi!")

if __name__ == "__main__":
    seed()
