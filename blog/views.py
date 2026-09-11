from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator

# Create your views here.
from .models import Post, Category, Tag, Comment
from .forms import PostForm, CommentForm


def home_view(request):
    now = timezone.now()
    week_ago = now - timedelta(days=7)
    month_ago = now - timedelta(days=30)

    # Baza queryset - faqat admin tasdiqlagan postlar
    base_qs = Post.objects.filter(is_approved=True).select_related("author", "category").prefetch_related("tags")

    # Tavsiya etilgan postlar (Banner / alohida blok uchun)
    recommended_posts = base_qs.filter(is_recommended=True)[:4]

    # Eng ko'p ko'rilgan postlar (Yon blok yoki tab uchun)
    most_viewed_posts = base_qs.order_by("-views_count")[:5]

    # Haftaning eng ommabop postlari (oxirgi 7 kundagi)
    weekly_popular = base_qs.filter(created_at__gte=week_ago).order_by("-views_count")[:6]
    weekly_qs = base_qs.filter(created_at__gte=week_ago).order_by("-views_count")
    weekly_popular = weekly_qs[:6]
    if not weekly_popular.exists():
        weekly_popular = most_viewed_posts[:6]

    # Oyning eng ommabop postlari (oxirgi 30 kundagi)
    monthly_popular = base_qs.filter(created_at__gte=month_ago).order_by("-views_count")[:6]
    monthly_qs = base_qs.filter(created_at__gte=month_ago).order_by("-views_count")
    monthly_popular = monthly_qs[:6]
    if not monthly_popular.exists():
        monthly_popular = most_viewed_posts[:6]

    # Tab filtrini olish
    tab = request.GET.get("tab", "latest")
    q = request.GET.get("q", "").strip()

    if q:
        posts_list = base_qs.filter(
            Q(title__icontains=q) | Q(content__icontains=q) | Q(tags__name__icontains=q)
        ).distinct()
        tab_title = f"'{q}' bo'yicha qidiruv natijalari"
    elif tab == "most_viewed":
        posts_list = base_qs.order_by("-views_count")
        tab_title = "Eng ko'p ko'rilgan postlar"
    elif tab == "weekly":
        posts_list = weekly_popular
        posts_list = weekly_qs if weekly_qs.exists() else base_qs.order_by("-views_count")
        tab_title = "Haftaning eng ommabop postlari"
    elif tab == "monthly":
        posts_list = monthly_popular
        posts_list = monthly_qs if monthly_qs.exists() else base_qs.order_by("-views_count")
        tab_title = "Oyning eng ommabop postlari"
    elif tab == "recommended":
        posts_list = base_qs.filter(is_recommended=True)
        tab_title = "Tavsiya qilingan postlar"
    else:
        # Standart: Eng yangi postlar
        posts_list = base_qs.order_by("-created_at")
        tab_title = "Eng yangi postlar"

    # Sahifalash (Pagination)
    paginator = Paginator(posts_list, 6)
    page_number = request.GET.get("page")
    posts = paginator.get_page(page_number)

    context = {
        "posts": posts,
        "recommended_posts": recommended_posts,
        "most_viewed_posts": most_viewed_posts,
        "weekly_popular": weekly_popular,
        "monthly_popular": monthly_popular,
        "current_tab": tab,
        "tab_title": tab_title,
        "search_query": q,
    }
    return render(request, "blog/home.html", context)


def post_detail_view(request, slug):
    # Oddiy foydalanuvchilar faqat tasdiqlangan yoki o'zi muallif bo'lgan postni ko'ra oladi
    if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
        post = get_object_or_404(Post, slug=slug)
    elif request.user.is_authenticated:
        post = get_object_or_404(Post.objects.filter(Q(is_approved=True) | Q(author=request.user)), slug=slug)
    else:
        post = get_object_or_404(Post, slug=slug, is_approved=True)

    # Ko'rishlar sonini oshirish (session orqali qayta hisoblashning oldi olinadi)
    session_key = f"viewed_post_{post.id}"
    if not request.session.get(session_key, False):
        Post.objects.filter(id=post.id).update(views_count=post.views_count + 1)
        post.views_count += 1
        request.session[session_key] = True

    # Izoh qoldirish
    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.warning(request, "Izoh qoldirish uchun tizimga kiring.")
            return redirect(f"/accounts/login/?next={request.path}")
        
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, "Izohingiz muvaffaqiyatli qo'shildi!")
            return redirect("blog:post_detail", slug=post.slug)
    else:
        comment_form = CommentForm()

    comments = post.comments.select_related("author").order_by("-created_at")
    
    # O'xshash postlar (bir xil bo'limdagi)
    related_posts = Post.objects.filter(
        category=post.category, is_approved=True
    ).exclude(id=post.id)[:3]

    context = {
        "post": post,
        "comments": comments,
        "comment_form": comment_form,
        "related_posts": related_posts,
    }
    return render(request, "blog/post_detail.html", context)


@login_required
def post_create_view(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.is_approved = False  # Admin tasdiqlashi shart
            post.save()
            form.save_m2m()  # Teglarni bog'lash
            
            messages.success(
                request,
                "Postingiz muvaffaqiyatli qabul qilindi! Admin tasdiqlagandan so'ng asosiy sahifada ko'rinadi."
            )
            return redirect("blog:my_posts")
    else:
        form = PostForm()

    return render(request, "blog/post_create.html", {"form": form})


@login_required
def my_posts_view(request):
    # Foydalanuvchining barcha postlari (tasdiqlangan va kutilayotganlar)
    user_posts = Post.objects.filter(author=request.user).order_by("-created_at")
    paginator = Paginator(user_posts, 10)
    page_number = request.GET.get("page")
    posts = paginator.get_page(page_number)

    return render(request, "blog/my_posts.html", {"posts": posts})


def category_posts_view(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts_list = Post.objects.filter(category=category, is_approved=True).order_by("-created_at")
    paginator = Paginator(posts_list, 6)
    page_number = request.GET.get("page")
    posts = paginator.get_page(page_number)

    return render(request, "blog/category_posts.html", {
        "category": category,
        "posts": posts,
    })


def tag_posts_view(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    posts_list = Post.objects.filter(tags=tag, is_approved=True).order_by("-created_at")
    paginator = Paginator(posts_list, 6)
    page_number = request.GET.get("page")
    posts = paginator.get_page(page_number)

    return render(request, "blog/tag_posts.html", {
        "tag": tag,
        "posts": posts,
    })
