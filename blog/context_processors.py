from .models import Category, Tag, Post
from django.db.models import Count, Q


def blog_globals(request):
    # Faqat tasdiqlangan postlarga ega bo'limlarni sanaymiz
    categories = Category.objects.annotate(
        approved_posts_count=Count("posts", filter=Q(posts__is_approved=True))
    )
    tags = Tag.objects.all()[:20]
    
    user_pending_count = 0
    if request.user.is_authenticated:
        if request.user.is_staff:
            user_pending_count = Post.objects.filter(is_approved=False).count()
        else:
            user_pending_count = Post.objects.filter(author=request.user, is_approved=False).count()

    return {
        "global_categories": categories,
        "global_tags": tags,
        "pending_posts_count": user_pending_count,
    }

