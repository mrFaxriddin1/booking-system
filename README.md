# Booking System

A Django REST API + HTML booking system with slot-based scheduling, race-condition-safe bookings, and Celery reminders.

🇺🇿 [O'zbekcha](#ozbekcha) | 🇬🇧 [English](#english)

---

## English

A small but production-minded booking system built to demonstrate real backend engineering problems: concurrent booking conflicts, background task scheduling, and clean API design.

### Features
- Service / Provider / Working hours / Booking models
- Available-slot calculation based on working hours and existing bookings
- **Race-condition-safe booking creation** using `select_for_update()` — verified with a concurrent-thread test
- REST API (Django REST Framework)
- Simple server-rendered HTML booking flow
- Automatic reminder emails/SMS scheduled via **Celery + Redis**, triggered by a model signal regardless of how a booking was created (admin, API, or HTML form)
- Automated tests, including a dedicated race-condition test

### Tech stack
Django · Django REST Framework · PostgreSQL · Celery · Redis · uv

### Setup
```bash
git clone https://github.com/<mrFaxriddin1>/booking-system.git
cd booking-system
uv sync
cp .env.example .env   # fill in your own values
uv run python manage.py migrate
uv run python manage.py createsuperuser
uv run python manage.py runserver
```

In a separate terminal:
```bash
uv run celery -A config worker -l info
```

### Tests
```bash
uv run python manage.py test
```

### Key design decision: preventing double-booking

A naive "check then save" approach has a race condition: two requests arriving at nearly the same time can both pass validation before either is saved. This project solves it with `select_for_update()` inside a DB transaction, locking the provider row so a second request waits until the first commits. This is verified in `bookings/tests/test_services.py` using real concurrent threads.

---

## Ozbekcha

Vaqt oralig'iga asoslangan bron tizimi — real backend muammolarini (parallel bronlar to'qnashuvi, fon vazifalari, toza API dizayni) hal qilish uchun qurilgan.

### Imkoniyatlar
- Service / Provider / Ish vaqti / Booking modellari
- Ish vaqti va mavjud bronlarga asoslangan bo'sh slotlarni hisoblash
- **Race condition'dan himoyalangan** bron yaratish (`select_for_update()`) — parallel thread testi bilan tasdiqlangan
- REST API (Django REST Framework)
- Server tomonida render qilinadigan oddiy HTML bron oqimi
- **Celery + Redis** orqali avtomatik eslatmalar — bron qanday yaratilishidan qat'iy nazar (admin, API yoki HTML forma) signal orqali ishga tushadi
- Avtomatik testlar, shu jumladan race condition uchun alohida test

### Texnologiyalar
Django · Django REST Framework · PostgreSQL · Celery · Redis · uv

### O'rnatish
```bash
git clone https://github.com/<mrFaxriddin1>/booking-system.git
cd booking-system
uv sync
cp .env.example .env   # o'z qiymatlaringizni kiriting
uv run python manage.py migrate
uv run python manage.py createsuperuser
uv run python manage.py runserver
```

Alohida terminalda:
```bash
uv run celery -A config worker -l info
```

### Testlar
```bash
uv run python manage.py test
```

### Asosiy arxitektura qarori: qo'sh bronni oldini olish

"Avval tekshir, keyin saqla" yondashuvida race condition bor: ikki so'rov deyarli bir vaqtda kelsa, ikkalasi ham bir-birini ko'rmasdan tekshiruvdan o'tib ketishi mumkin. Bu loyihada muammo `select_for_update()` bilan hal qilingan — DB transaction ichida provider qatori qulflanadi, ikkinchi so'rov birinchisi tugaguncha kutadi. Bu `bookings/tests/test_services.py` faylida haqiqiy parallel thread'lar bilan tasdiqlangan.