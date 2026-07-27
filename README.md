# Mentored

Образовательная платформа Ирины Карбоновой: курсы, книги, консультации 1:1 и
membership-подписка с онлайн-оплатой через Mercado Pago (Перу).

**Версия: 1.0** — первый боевой релиз, полный цикл "зарегистрировался → выбрал
товар → оплатил → заказ виден в личном кабинете и в админке" работает и
проверен реальным платежом.

Прод: https://www.mentoredgroup.com

---

## Возможности (v1.0)

### Пользователи
- Регистрация и вход по email (JWT, `djangorestframework-simplejwt`)
- Личный кабинет: профиль, смена данных, история заказов ("Mis pedidos")
- Разграничение прав: обычный пользователь / суперюзер (админка Django)

### Каталог
- Товары четырёх типов: курсы, книги, консультации, membership
- Общий список/детальная страница по slug (`/products/`)
- Блог с категориями

### Корзина и заказы
- Корзина у каждого пользователя (add/update/remove/clear)
- Оформление заказа "замораживает" цену и данные товара на момент покупки
  (`OrderItem` не зависит от дальнейших изменений цены товара)
- История заказов и статус каждого (`pending` → `paid` / `cancelled` / `refunded`)

### Оплата — Mercado Pago Checkout Pro
- Создание preference и редирект на хостед-чекаут Mercado Pago
- Webhook (`/payment/webhook/`) обрабатывает уведомления об оплате:
  запрашивает реальный статус платежа через API MP, обновляет `Order` и
  `Payment`, проверяет подпись `x-signature` (если задан `MERCADOPAGO_WEBHOOK_SECRET`)
- Валюта — PEN (Перу), настраивается через `.env`
- Проверено реальным платежом на проде (см. `Payment` в админке)

### Обратная связь
- Форма на странице "Contacto" сохраняет заявки в БД, опционально шлёт
  email-уведомление (нужны SMTP-креды в `.env`)

### Админка (`/admin/`)
- Пользователи, товары (курсы/книги/консультации/membership), блог
- Заказы (с товарами внутри) и платежи — фильтры по статусу, поиск по
  email/номеру заказа/ID транзакции
- Заявки с формы контактов

---

## Технологии

| Слой | Стек |
|---|---|
| Backend | Django 4.2 + Django REST Framework, JWT (simplejwt) |
| БД | PostgreSQL 16 |
| Frontend | Vue 3 + Vite |
| Оплата | Mercado Pago SDK (Checkout Pro) |
| Инфра | Docker Compose, nginx (SSL/Let's Encrypt), деплой на VPS |

## Структура проекта

```
backend/
  config/        - настройки Django, корневой urls.py
  mentored/      - основное приложение: пользователи, товары, блог,
                   корзина, заказы, форма контактов
  payments/      - интеграция с Mercado Pago (preference, webhook, Payment)
frontend/
  src/api/       - обёртки над axios для каждого раздела бэкенда
  src/views/     - страницы (Vue SFC)
  src/router/    - маршруты SPA
docker-compose.yml
```

## API (основные эндпоинты)

```
POST   /token/                     получить JWT (email + password)
POST   /register/                  регистрация
GET    /profile/                   профиль текущего пользователя

GET    /products/                  список товаров
GET    /products/<slug>/           товар по slug
GET    /blog/posts/                посты блога

GET    /cart/                      корзина
POST   /cart/add/                  добавить товар
POST   /create_order/              оформить заказ из корзины
GET    /orders/                    история заказов
GET    /orders/<order_number>/     заказ по номеру

POST   /payment/create-preference/ создать платёж (Mercado Pago)
POST   /payment/webhook/           приём уведомлений от Mercado Pago

POST   /contact/                   форма обратной связи
```

## Запуск локально

```bash
cp .env.example .env   # заполнить POSTGRES_*, MERCADOPAGO_* и т.д.
docker-compose up -d --build
docker exec mentored_backend python manage.py migrate
```

Бэкенд — `localhost:8000`, фронт собирается в `frontend/dist` и отдаётся
через nginx на `localhost`.

## Известные ограничения / что не готово

- Отдельные списки по типам товара (`/courses/`, `/books/`,
  `/consultations/`, `/memberships/`) закомментированы в `urls.py` — сейчас
  всё отдаётся через общий `/products/`
- Email-уведомления формы контактов не настроены (нет SMTP в `.env`)
- `DEBUG=True` и `ALLOWED_HOSTS=['*']` — дефолтные настройки Django,
  стоит ужесточить перед дальнейшим ростом нагрузки

---

Технический документ по следующему этапу — в процессе (см. историю задач).
