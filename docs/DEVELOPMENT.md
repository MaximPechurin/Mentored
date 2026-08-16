# Mentored — техническая документация для разработчика

Образовательная платформа: интернет-магазин (курсы/книги/консультации/
membership) + учебная платформа (LMS). Прод: https://www.mentoredgroup.com

Этот документ — про **как устроен код** и **как с ним работать**. Обзор
возможностей для пользователя — в `README.md`, план и статус Этапа 2 —
в `PLAN_ETAP2.md`.

---

## 1. Стек

| Слой | Технология |
|---|---|
| Backend | Django 4.2 + Django REST Framework, JWT (`djangorestframework-simplejwt`) |
| БД | PostgreSQL 16 |
| Frontend | Vue 3 + Vite, Pinia, Vue Router, axios |
| Оплата | Mercado Pago SDK (Checkout Pro) |
| Инфра | Docker Compose, nginx (SSL/Let's Encrypt), VPS |

---

## 2. Структура репозитория

```
Mentored/
  backend/
    config/        настройки, корневой urls.py, кастомный AdminSite
    mentored/      «магазин»: пользователи, роли, товары, корзина, заказы, блог, контакты
    payments/      Mercado Pago: preference + webhook + Payment
    school/        «учебная платформа» (LMS): курсы, уроки, доступы, прогресс, ДЗ, форум, ЛС
    requirements.txt
    Dockerfile
  frontend/
    src/
      api/         обёртки axios по разделам (auth, products, cart, orders, school, ...)
      components/  Header, Footer, EscuelaNav (шапка школы), ChatWidget
      composables/ useAuth, useLanguage (витрина), useSchoolLang (школа, ES/RU/EN)
      views/       страницы; views/escuela/* — учебная платформа
      router/
  docker-compose.yml
  docs/DEVELOPMENT.md   (этот файл)
  PLAN_ETAP2.md
```

---

## 3. Ключевая архитектурная идея: два «курса»

В системе **две разные сущности со словом «курс»** — не путать:

- **`mentored.Course`** — ТОВАР в магазине (цена, обложка, slug для витрины,
  участвует в корзине/заказах/Mercado Pago). Один из четырёх типов товара
  (`Book`, `Course`, `Consultation`, `Membership`, все наследуют абстрактный
  `Product`).
- **`school.Course`** — УЧЕБНЫЙ курс (контент: модули → уроки → материалы →
  задания, плюс прогресс студентов). Не знает про цену и оплату.

Связывает их **`school.ProductCourseAccess`** — «какой товар открывает доступ
к какому учебному курсу». Товар в этой связке — generic (`ContentType` +
`object_id`, как в `mentored.CartItem`), поэтому:
- один товар может открывать несколько учебных курсов (Membership → все курсы),
- несколько товаров могут вести к одному курсу (акционный бандл).

Зачем так: учебную часть можно менять, не задевая модель товара, от которой
зависит боевая оплата.

---

## 4. Модели `school` (`backend/school/models.py`)

```
Course ─┬─ Module ── Lesson ─┬─ LessonMaterial
        │                    └─ Assignment ── Submission (ответ студента + проверка)
        ├─ CourseTeacher (кто ведёт курс: FK course + FK user)
        ├─ ProductCourseAccess (generic товар → курс)
        └─ Enrollment (доступ студента) ── LessonProgress (прогресс по уроку)

TeacherProfile (OneToOne user)         — витринная карточка препода (задел на Этап 3)
ForumThread ── ForumPost               — форум курса (публичные обсуждения)
DirectMessage                          — личные сообщения 1:1
```

Важное:
- **`Enrollment`** (`user`, `course`, `is_active`, `order_item`) — «право доступа
  прямо сейчас». Кабинет студента читает курсы отсюда, а не из заказов. Уникален
  на пару `(user, course)`. Отзыв доступа = `is_active=False` (прогресс не теряется).
- **`LessonProgress`** — по строке на `(enrollment, lesson)`: `is_completed`,
  `last_position_seconds`.
- **`Submission`** — одна «текущая» сдача на `(assignment, enrollment)`; пересдача
  обновляет её и сбрасывает статус в `submitted`. Статусы: `submitted` /
  `reviewed` / `needs_revision`.
- Хелперы доступа к общению (в конце `models.py`): `is_course_participant`,
  `is_course_teacher`, `can_direct_message` (личка — только между студентом и
  преподавателем общего курса).

---

## 5. Роли и доступ

- **`mentored.Role`** — роль отдельной моделью (не `choices`), `codename`
  (`student`/`teacher`). У `User` — `roles = M2M(Role)` (можно совмещать).
  Хелперы: `user.has_role(codename)`, `user.is_teacher`, `user.is_student`.
  Сиды ролей — миграция `mentored/0007_seed_roles`.
- При регистрации пользователю автоматически выдаётся роль `student`
  (`RegisterSerializer.create`).
- **`User.is_dev`** — временный feature-flag: раздел «Школа» на проде открыт
  только пользователям с этой галкой (и суперюзерам). Гейт двойной —
  на фронте (редирект) и в API (`school.permissions.IsDev`). Когда школу
  откроют всем — снять `IsDev` со school-вью и `is_dev`-условия на фронте.
- **DRF-permissions** (`school/permissions.py`): `IsDev`, `IsStudent`,
  `IsTeacher`. Проверка доступа к конкретному курсу — через `Enrollment`
  (студент) и `CourseTeacher` (преподаватель), не только по роли.
- В **админке** преподаватель (не суперюзер) видит только свои курсы и
  связанные объекты — `TeacherScopedAdminMixin` в `school/admin.py`.

---

## 6. Хук «оплата → доступ»

`school/signals.py`: сигнал `post_save` на `mentored.Order` (подключён в
`school/apps.py::ready()`). При статусе заказа `paid` для каждого `OrderItem`
резолвится товар (`ContentType` строго `app_label='mentored'` + `product_id`),
по нему берутся все `ProductCourseAccess` и создаётся `Enrollment` на каждый
учебный курс (идемпотентно, без дублей; не реактивирует вручную отозванный
доступ; заодно проставляет роль `student`). Покрывает и вебхук Mercado Pago,
и ручную смену статуса в админке. Ошибки только логируются — оплату не роняет.

---

## 7. API учебной платформы (префикс `/school/`)

Все эндпоинты требуют JWT + `IsDev`. Студенческие — `IsStudent`, преподавательские
— `IsTeacher`.

**Студент:**
```
GET  /school/my-courses/                     купленные курсы + прогресс
GET  /school/courses/<slug>/                 модули → уроки → материалы/задания
POST /school/lessons/<id>/progress/          {is_completed, last_position_seconds}
GET  /school/assignments/<id>/               задание + мой ответ
POST /school/assignments/<id>/submit/        сдать (multipart: text и/или file)
```

**Преподаватель:**
```
GET  /school/teacher/courses/                мои курсы + счётчики
GET  /school/teacher/courses/<id>/students/  ростер студентов с прогрессом
GET  /school/teacher/courses/<id>/analytics/ сводка по курсу
GET  /school/teacher/submissions/            очередь ДЗ (?status=all|<status>)
POST /school/teacher/submissions/<id>/review/ {status, score, mentor_comment}
```

**Форум курса** (участники = студенты + преподаватели курса):
```
GET/POST /school/courses/<id>/threads/       список / создать тему
GET      /school/threads/<id>/               тема + сообщения
POST     /school/threads/<id>/posts/         ответить
POST     /school/threads/<id>/moderate/      pin/lock (только препод)
```

**Чат / личные сообщения** (студент ↔ преподаватель общего курса):
```
GET      /school/chat/directory/             дерево чата + непрочитанные (role-aware)
GET      /school/messages/                   список диалогов
GET/POST /school/messages/<user_id>/         переписка / отправка (GET помечает прочитанным)
```

**Аналитика:**
```
GET /school/analytics/overview/              общая по платформе (только суперюзер)
```

Auth/магазин (приложение `mentored`): `/token/`, `/token/refresh/`, `/register/`,
`/profile/` (отдаёт `roles`, `is_dev`), `/products/`, `/cart/*`, `/create_order/`,
`/orders/*`; оплата — `/payment/*` (приложение `payments`).

> Замечание: глобально в DRF включён только `JSONParser`
> (`settings.REST_FRAMEWORK`). Для загрузки файла (`assignments/<id>/submit/`)
> multipart-парсер добавлен точечно на вью. На фронте axios-интерцептор
> (`src/api/index.js`) снимает дефолтный `Content-Type: application/json` для
> `FormData`, иначе файл не долетает. Файловые поля отдаются абсолютным URL
> (в сериализатор прокинут `request`).

---

## 8. Frontend: учебная платформа

- Роут `/escuela/*` = отдельная «учебная платформа». В `App.vue` для этих
  путей маркетинговый `Header`/`Footer` скрыт, вместо него тёмная шапка
  `EscuelaNav`; на этих же страницах монтируется `ChatWidget` (чат справа снизу).
- Страницы: `EstudianteCabinetPage` (мои курсы), `EscuelaCoursePage` (курс,
  уроки, видео, материалы, сдача ДЗ), `ProfesorCabinetPage` (курсы, ростер
  студентов, очередь ДЗ + проверка прямо тут).
- Доступ к разделу: `is_dev` + роль; иначе редирект (см. `onMounted` страниц).
- **i18n школы** — `composables/useSchoolLang.js`: свой стейт (ключ
  `school_lang` в localStorage), словари **ES/RU/EN**, функция `st('...')`,
  фолбэк на ES. Полностью независим от языка витрины (`useLanguage`), которую
  не трогаем (остаётся на испанском). Переводится только интерфейс; контент
  курсов (названия/тексты уроков) — как заведён в админке.
- **Чат** (`ChatWidget.vue`): плавающая кнопка → дерево (курс → собеседник) →
  переписка; красные точки непрочитанного на всех уровнях; поллинг раз в 15с.

---

## 9. Кастомная админка

- `config/admin.py` — `MentoredAdminSite` (подключён через
  `config/apps.py::MentoredAdminConfig`, заменяет `django.contrib.admin` в
  `INSTALLED_APPS`). `get_app_list` разбивает модели `school` на блоки:
  «Работа с курсами», «Студенты и доступы», «Общение».
- Гайд для контент-менеджера — на главной админки
  (`school/templates/admin/guia_index.html`, подключён через `index_template`).

---

## 10. Локальный запуск (Docker)

```bash
cd Mentored
cp .env.example .env          # заполнить POSTGRES_*, MERCADOPAGO_* (для теста — заглушки)
cp .env backend/.env          # backend читает .env из своей папки (Dockerfile: collectstatic)

docker compose up -d --build db backend
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py createsuperuser

# фронт: сборка через контейнер frontend (compose) ИЛИ vite dev:
#   docker run -d --name mentored_front_dev --network host \
#     -v $PWD/frontend:/app -w /app node:20-alpine \
#     sh -c "npm install && npm run dev -- --host 0.0.0.0 --port 5173"
```

Бэкенд — `:8000`, фронт (vite dev) — `:5173`, админка — `/admin/`.
`config/settings.py`: `DEBUG=True` (dev), `CORS_ALLOWED_ORIGINS` включает
localhost:5173, media/статика отдаются при DEBUG.

Прогон валидации без боевой БД (миграции/тесты на sqlite) — как в CI:
подменить `DATABASES` на sqlite в отдельном settings-модуле и гнать
`manage.py check` / `migrate`.

---

## 11. Ветки и деплой

- **`dev`** — рабочая ветка разработки (весь Этап 2). `main`/`test` —
  «боевое» состояние.
- **Прод**: VPS, проект в `/projects/Mentored`, ветка `main`, стек в Docker
  Compose (db + backend + frontend + nginx).
- **Порядок деплоя** (в папке проекта на сервере):
  ```bash
  docker compose exec -T db pg_dump -U mentored_user mentored > ~/backup_$(date +%F_%H%M).sql
  git pull origin main
  docker compose exec -T backend python manage.py migrate   # сразу после pull
  docker compose restart frontend backend
  docker compose ps
  ```
  **Миграции обязательны** вместе с кодом: код Этапа 2 зависит от новых полей
  (`Role`, `is_dev`, приложение `school`) — без `migrate` регистрация/профиль
  упадут.
- Почта (уведомления школы, форма контактов) — SMTP из `.env`; если не
  настроено, письма не шлются (best-effort, операции не роняются).

---

## 12. Полезные заметки

- Slug учебного курса генерируется из названия с `allow_unicode=True`
  (поддержка кириллицы) + числовой суффикс при коллизии.
- `OrderItem` хранит замороженные `product_type` (имя модели, напр. `course`)
  и `product_id` — это исторический слепок покупки, не живой FK.
- Realtime в чате пока нет — обновление опросом (15с). При необходимости
  «секунда-в-секунду» — WebSocket/Django Channels (отдельная задача).
