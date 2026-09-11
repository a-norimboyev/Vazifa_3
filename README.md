# 🌟 BlogSphere — Django Blog Loyihasi

Django freymvorki yordamida yaratilgan template-based zamonaviy blog platformasi. Ushbu loyihada foydalanuvchilar ro'yxatdan o'tib o'z maqolalarini chop etishlari, izoh qoldirishlari va administrator tomonidan tasdiqlangan postlar asosiy sahifada aks etishi ta'minlangan.

---

## 🚀 Loyiha Imkoniyatlari va Talablarning Bajarilishi

### 1. 📝 Postlar Tizimi:
- **Sarlavha (Title)** va **Matn (Content)**;
- **Rasm (Image)** — har bir maqola uchun muqova rasmi (agar rasm yuklanmasa, mos vizual placeholder ko'rsatiladi);
- **Bo'limi (Category)** — maqolalarni bo'limlar bo'yicha guruhlash;
- **Teglari (Tags)** — ko'pdan-ko'pga (ManyToMany) bog'langan teglar, post yaratishda yangi teglarni kiritish imkoniyati.

### 2. 💬 Izohlar Tizimi:
- Har bir post sahifasida (detail view) izohlar ro'yxati aks etadi;
- Ro'yxatdan o'tgan foydalanuvchilar har bir maqolaga o'z fikr-mulohazalarini yozib qoldirishlari mumkin.

### 3. 👤 Foydalanuvchi Tizimi (Autentifikatsiya):
- **Ro'yxatdan o'tish (Register)**: foydalanuvchi nomi, ism-familiya, email va xavfsiz parol tekshiruvi;
- **Kirish (Login)** va **Chiqish (Logout)**;
- **Post qo'shish**: Har bir kirgan foydalanuvchi o'z postini qo'sha oladi;
- **Mening postlarim**: Foydalanuvchi o'zi yozgan barcha postlar holatini (tasdiqlangan yoki kutilmoqda) ko'rib boradi.

### 4. 🛡️ Admin Tasdiqlash (Moderatsiya):
- Foydalanuvchilar tomonidan yozilgan har qanday yangi post avtomatik tarzda **kutilmoqda (is_approved=False)** holatida bo'ladi;
- Asosiy veb-saytda va ommaviy ro'yxatlarda faqat admin tasdiqlagan (is_approved=True) postlar chiqadi;
- Tasdiqlanmagan postlar oddiy tashrif buyuruvchilarga ko'rinmaydi (faqat muallifning o'zi va administrator ko'ra oladi);
- Django Admin panelida bir nechta postlarni bitta tugma orqali tasdiqlash uchun maxsus aksiyalar (pprove_posts, unapprove_posts, make_recommended) mavjud.

### 5. 🏠 Asosiy Sahifa va Filtrlash:
Asosiy sahifada qulay filtr tablari va maxsus bloklar mavjud:
- 🆕 **Eng yangi postlar** (?tab=latest)
- 🔥 **Eng ko'p ko'rilgan postlar** (?tab=most_viewed)
- 📅 **Haftaning eng ommabop postlari** (?tab=weekly — oxirgi 7 kundagi ko'rishlar bo'yicha)
- 📊 **Oyning eng ommabop postlari** (?tab=monthly — oxirgi 30 kundagi ko'rishlar bo'yicha)
- ⭐ **Tavsiya qilingan postlar** (?tab=recommended va bosh sahifa yuqorisidagi alohida tavsiya bloki)
- 🔍 Sarlavha, matn va teglar bo'yicha qidiruv.

---

## 🛠️ O'rnatish va Ishga Tushirish

### 1. Repozitoriyani klonlash:
`ash
git clone https://github.com/a-norimboyev/Vazifa_3.git
cd Vazifa_3
`

### 2. Virtual muhit yaratish va faollashtirish:
`ash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux / MacOS
python3 -m venv .venv
source .venv/bin/activate
`

### 3. Talab qilinadigan kutubxonalarni o'rnatish:
`ash
pip install -r requirements.txt
`

### 4. Ma'lumotlar bazasi migratsiyasini bajarish:
`ash
python manage.py migrate
`

### 5. Namunaviy ma'lumotlarni yuklash (Seed data):
Loyiha ichidagi tayyor skript orqali demo kategoriyalar, teglar, rasmli maqolalar, admin va test foydalanuvchilarni bitta buyruq bilan yaratishingiz mumkin:
`ash
python seed_data.py
`

### 6. Loyihani ishga tushirish:
`ash
python manage.py runserver
`
Brauzerda http://127.0.0.1:8000/ manzilini oching.

---

## 🔑 Sinov Akkauntlari (Seed Data orqali yaratiladi)

- **Admin (Superuser):**
  - Login: dmin
  - Parol: dmin123
  - Admin panel manzili: http://127.0.0.1:8000/admin/

- **Foydalanuvchi 1:**
  - Login: javohir
  - Parol: 	estpass123

- **Foydalanuvchi 2:**
  - Login: 
odira
  - Parol: 	estpass123

---

## 🧪 Avtomatlashtirilgan Testlarni Ishga Tushirish

Loyiha uchun to'liq test ssenariylari yozilgan:
`ash
python manage.py test
`
Barcha testlar tizim talablari (tasdiqlash, ruxsatlar, ko'rishlar soni, sahifalash va izohlar) to'g'ri ishlashini tekshiradi.
