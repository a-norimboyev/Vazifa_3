from django import forms
from .models import Post, Comment, Category, Tag


class PostForm(forms.ModelForm):
    new_tags = forms.CharField(
        required=False,
        label="Yangi teglar",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "masalan: texnologiya, yangiliklar, suniy_intellekt"
        }),
        help_text="Vergul bilan ajratib yozing. Mavjud teglardan tashqari yangi teglar qo'shishingiz mumkin"
    )

    class Meta:
        model = Post
        fields = ["title", "category", "tags", "image", "content"]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Post sarlavhasini kiriting..."
            }),
            "category": forms.Select(attrs={
                "class": "form-select"
            }),
            "tags": forms.SelectMultiple(attrs={
                "class": "form-select",
                "size": "4"
            }),
            "image": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),
            "content": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 8,
                "placeholder": "Postning to'liq matnini shu yerga yozing..."
            }),
        }

    def save(self, commit=True):
        instance = super().save(commit=commit)
        new_tags_str = self.cleaned_data.get("new_tags", "")
        if new_tags_str:
            tag_names = [t.strip().lstrip("#") for t in new_tags_str.split(",") if t.strip()]
            tags_to_add = [Tag.objects.get_or_create(name=name)[0] for name in tag_names]
            
            old_save_m2m = getattr(self, "save_m2m", None)
            def save_m2m():
                if old_save_m2m:
                    old_save_m2m()
                instance.tags.add(*tags_to_add)
            
            self.save_m2m = save_m2m
            if commit:
                instance.tags.add(*tags_to_add)
        return instance


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Fikringizni yoki izohingizni yozib qoldiring..."
            }),
        }
        labels = {
            "content": "",
        }

