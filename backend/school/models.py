from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.text import slugify

from mentored.utils import get_upload_path

# ============================================================
# Этап 2 (School): структура данных для курсов, уроков, прогресса
# и домашних заданий.
#
# Архитектурное решение (обсуждено и согласовано в чате):
# - `mentored.Course` остаётся ТОВАРОМ для каталога/оплаты как есть
#   (цена, slug для витрины, Mercado Pago и т.д.) - не трогаем, чтобы
#   не задеть корзину/заказы.
# - Учебный контент - самостоятельная сущность `school.Course` (модули,
#   уроки, прогресс, задания висят на ней, а не на товаре напрямую).
#   Может существовать даже без привязанного товара (бесплатный курс).
# - Связь "какой товар открывает доступ к какому учебному курсу" - не
#   жёсткий FK, а отдельная модель `ProductCourseAccess`, товар в ней -
#   generic (как уже сделано в mentored.CartItem), а не захардкожен на
#   mentored.Course. Так один товар может открывать несколько курсов
#   (например Membership -> все курсы), а несколько товаров - вести к
#   одному и тому же курсу (акционный бандл), без хардкода в коде хука
#   "оплата -> доступ".
# ============================================================


class TeacherProfile(models.Model):
    """
    Профиль преподавателя/ментора - данные для кабинета преподавателя и
    задел на будущую публичную карточку ментора на сайте (ТЗ, Этап 3:
    "Профили менторов с квалификацией"). На Этапе 2 `is_public` не
    используется фронтом сайта - поле просто заранее зарезервировано,
    чтобы не переделывать модель, когда дойдём до публичных страниц.

    Заводится на пользователя с ролью `Role.TEACHER` (роль и профиль -
    разные вещи: роль даёт права в системе, профиль - витринные данные).
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='teacher_profile',
        verbose_name='Пользователь',
    )
    photo = models.ImageField(
        upload_to=get_upload_path,
        blank=True,
        null=True,
        verbose_name='Фото',
    )
    specialization = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Специализация',
        help_text='Например: коуч, психолог, ментор по продажам',
    )
    bio = models.TextField(blank=True, verbose_name='О себе')
    is_public = models.BooleanField(
        default=False,
        verbose_name='Показывать на сайте',
        help_text='Публичная карточка ментора появится в Этапе 3 - пока просто задел на будущее',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Профиль преподавателя'
        verbose_name_plural = 'Профили преподавателей'

    def __str__(self):
        return f"Профиль ментора: {self.user.email}"


class Course(models.Model):
    """
    Учебный курс - САМОСТОЯТЕЛЬНАЯ сущность, отдельная от товара
    `mentored.Course` (витрина/цена/Mercado Pago). Модули и уроки
    привязаны именно сюда.

    Какой товар открывает доступ к этому курсу - решает не FK отсюда, а
    `ProductCourseAccess` (см. ниже): курс не обязан знать о товаре,
    товаров может быть несколько (или ни одного - бесплатный/ещё не
    выставленный на продажу курс).
    """
    title = models.CharField(max_length=255, verbose_name='Название курса')
    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True,
        allow_unicode=True,
        verbose_name='Слаг',
        help_text='Заполняется автоматически из названия, поддерживает кириллицу',
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание',
        help_text='Внутреннее описание для кабинета, не для маркетинговой витрины',
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активен',
        help_text='Можно временно скрыть курс из кабинетов, не удаляя контент и прогресс',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Учебный курс'
        verbose_name_plural = 'Учебные курсы'
        ordering = ['title']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            # allow_unicode=True - названия курсов у нас в основном на
            # русском (см. verbose_name везде в проекте), обычный slugify()
            # без этого флага вырезает кириллицу и даёт пустой слаг.
            base_slug = slugify(self.title, allow_unicode=True) or 'course'
            slug = base_slug
            n = 2
            # Два курса могут называться одинаково ("Курс личностного
            # роста" 2026 и 2027 набор) - на случай совпадения слага
            # добавляем числовой суффикс, а не падаем по unique=True.
            while Course.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{n}"
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)


class ProductCourseAccess(models.Model):
    """
    Связь "товар -> учебный курс, доступ к которому открывает покупка".

    Товар - любой (mentored.Course, в будущем Membership и т.д.) через
    GenericForeignKey, тем же способом, что уже использует
    `mentored.CartItem` - без хардкода конкретного типа товара в этой
    модели. Специально сделано гибко:
      - один товар может открывать сразу несколько курсов (Membership
        -> доступ ко всем текущим курсам - несколько строк с одним
        content_type/object_id и разными course)
      - несколько разных товаров могут вести к одному и тому же курсу
        (акционный бандл - несколько строк с разными товарами и одним
        course)

    При оплате заказа для каждого купленного товара ищутся все строки
    здесь, и по каждой найденной создаётся/активируется Enrollment.
    """
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        verbose_name='Тип товара',
    )
    object_id = models.PositiveIntegerField(verbose_name='ID товара')
    product = GenericForeignKey('content_type', 'object_id')

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='product_links',
        verbose_name='Учебный курс',
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания связи')

    class Meta:
        verbose_name = 'Доступ к курсу через товар'
        verbose_name_plural = 'Доступы к курсам через товары'
        constraints = [
            models.UniqueConstraint(
                fields=['content_type', 'object_id', 'course'],
                name='unique_product_course_access',
            ),
        ]

    def __str__(self):
        return f"{self.product} -> {self.course.title}"


class CourseTeacher(models.Model):
    """ Кто из преподавателей ведёт учебный курс. """
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='course_teachers',
        verbose_name='Курс',
    )
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='taught_courses',
        verbose_name='Преподаватель',
    )
    assigned_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата назначения')

    class Meta:
        verbose_name = 'Преподаватель курса'
        verbose_name_plural = 'Преподаватели курсов'
        constraints = [
            models.UniqueConstraint(fields=['course', 'teacher'], name='unique_course_teacher'),
        ]

    def __str__(self):
        return f"{self.teacher.email} ведёт «{self.course.title}»"


class Module(models.Model):
    """ Раздел (модуль) курса - группирует уроки по темам """
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='modules',
        verbose_name='Курс',
    )
    title = models.CharField(max_length=255, verbose_name='Название раздела')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Раздел курса'
        verbose_name_plural = 'Разделы курса'
        ordering = ['course', 'order']

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Lesson(models.Model):
    """ Урок внутри раздела: видео + текстовые материалы """
    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name='Раздел',
    )
    title = models.CharField(max_length=255, verbose_name='Название урока')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')
    video_url = models.URLField(
        blank=True,
        null=True,
        verbose_name='Ссылка на видео',
        help_text='Vimeo/YouTube/облако - плеер на фронте просто встраивает эту ссылку',
    )
    content = models.TextField(
        blank=True,
        verbose_name='Текст/описание урока',
    )
    duration_minutes = models.PositiveIntegerField(
        blank=True, null=True, verbose_name='Длительность (мин)',
    )
    is_free_preview = models.BooleanField(
        default=False,
        verbose_name='Бесплатный превью-урок',
        help_text='Доступен без покупки курса (например, первый урок для затравки)',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ['module', 'order']

    def __str__(self):
        return f"{self.module.title} - {self.title}"


class LessonMaterial(models.Model):
    """ Дополнительный файл к уроку (PDF, рабочая тетрадь и т.п.) """
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='materials',
        verbose_name='Урок',
    )
    title = models.CharField(max_length=255, verbose_name='Название материала')
    file = models.FileField(upload_to=get_upload_path, verbose_name='Файл')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Материал урока'
        verbose_name_plural = 'Материалы урока'
        ordering = ['id']

    def __str__(self):
        return f"{self.lesson.title} - {self.title}"


class Enrollment(models.Model):
    """
    Доступ студента к учебному курсу. Создаётся автоматически при
    оплате заказа (см. интеграцию оплата -> доступ через
    ProductCourseAccess), либо вручную из админки.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='enrollments',
        verbose_name='Студент',
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='enrollments',
        verbose_name='Курс',
    )
    order_item = models.ForeignKey(
        'mentored.OrderItem',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='enrollments',
        verbose_name='Заказ (откуда взялся доступ)',
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Доступ активен',
        help_text='Можно снять галочку, чтобы временно/навсегда отозвать доступ, не удаляя историю прогресса',
    )
    enrolled_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата открытия доступа')

    class Meta:
        verbose_name = 'Доступ к курсу'
        verbose_name_plural = 'Доступы к курсам'
        ordering = ['-enrolled_at']
        constraints = [
            models.UniqueConstraint(fields=['user', 'course'], name='unique_enrollment_per_user_course'),
        ]

    def __str__(self):
        return f"{self.user.email} -> {self.course.title}"


class LessonProgress(models.Model):
    """ Прогресс конкретного студента по конкретному уроку """
    enrollment = models.ForeignKey(
        Enrollment,
        on_delete=models.CASCADE,
        related_name='lesson_progress',
        verbose_name='Доступ к курсу',
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='progress_entries',
        verbose_name='Урок',
    )
    is_completed = models.BooleanField(default=False, verbose_name='Урок пройден')
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name='Дата завершения')
    last_position_seconds = models.PositiveIntegerField(
        default=0,
        verbose_name='Последняя позиция видео (сек)',
        help_text='Чтобы студент мог продолжить просмотр с того же места',
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Прогресс по уроку'
        verbose_name_plural = 'Прогресс по урокам'
        constraints = [
            models.UniqueConstraint(fields=['enrollment', 'lesson'], name='unique_progress_per_enrollment_lesson'),
        ]

    def __str__(self):
        status = 'пройден' if self.is_completed else 'в процессе'
        return f"{self.enrollment.user.email} - {self.lesson.title} ({status})"


class Assignment(models.Model):
    """ Домашнее задание, привязанное к уроку """
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='assignments',
        verbose_name='Урок',
    )
    title = models.CharField(max_length=255, verbose_name='Название задания')
    description = models.TextField(verbose_name='Описание задания')
    max_score = models.PositiveIntegerField(default=100, verbose_name='Максимальный балл')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Домашнее задание'
        verbose_name_plural = 'Домашние задания'
        ordering = ['lesson']

    def __str__(self):
        return f"{self.lesson.title} - {self.title}"


class Submission(models.Model):
    """ Ответ студента на домашнее задание + проверка ментором """
    STATUS_CHOICES = [
        ('submitted', 'Отправлено, ожидает проверки'),
        ('reviewed', 'Проверено'),
        ('needs_revision', 'Возвращено на доработку'),
    ]

    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name='submissions',
        verbose_name='Задание',
    )
    enrollment = models.ForeignKey(
        Enrollment,
        on_delete=models.CASCADE,
        related_name='submissions',
        verbose_name='Студент (доступ к курсу)',
    )
    text = models.TextField(blank=True, verbose_name='Текст ответа')
    file = models.FileField(
        upload_to=get_upload_path,
        blank=True,
        null=True,
        verbose_name='Файл ответа',
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='submitted',
        verbose_name='Статус',
    )
    score = models.PositiveIntegerField(null=True, blank=True, verbose_name='Оценка')
    mentor_comment = models.TextField(blank=True, verbose_name='Комментарий ментора')
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_submissions',
        verbose_name='Проверил',
    )
    submitted_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки')
    reviewed_at = models.DateTimeField(null=True, blank=True, verbose_name='Дата проверки')

    class Meta:
        verbose_name = 'Ответ на домашнее задание'
        verbose_name_plural = 'Ответы на домашние задания'
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.enrollment.user.email} - {self.assignment.title} ({self.get_status_display()})"
