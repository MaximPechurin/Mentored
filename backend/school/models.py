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
    video_file = models.FileField(
        upload_to=get_upload_path,
        blank=True,
        null=True,
        verbose_name='Видеофайл',
        help_text='Загруженный на сервер файл (mp4 и т.п.) - если заполнен, плеер '
                  'использует его вместо ссылки ниже; так поддерживается пересчёт '
                  'позиции просмотра (последняя минута сохраняется автоматически)',
    )
    video_url = models.URLField(
        blank=True,
        null=True,
        verbose_name='Ссылка на видео (запасной вариант)',
        help_text='Vimeo/YouTube/облако - используется только если видеофайл выше не загружен',
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
    is_public = models.BooleanField(
        default=False,
        verbose_name='Виден другим ученикам',
        help_text='По умолчанию ответ видят только автор и преподаватели; '
                  'ученик может открыть его для остальных студентов курса',
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


class SubmissionComment(models.Model):
    """
    Комментарий к ответу на домашнее задание (переписка под ответом,
    как в ленте ответов GetCourse-подобных LMS). Писать могут автор
    ответа и преподаватели курса; если ответ открыт (is_public) -
    любой активный студент курса.
    """
    submission = models.ForeignKey(
        Submission,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Ответ на задание',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='submission_comments',
        verbose_name='Автор',
    )
    text = models.TextField(verbose_name='Текст комментария')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата')

    class Meta:
        verbose_name = 'Комментарий к ответу'
        verbose_name_plural = 'Комментарии к ответам'
        ordering = ['created_at']

    def __str__(self):
        return f"{self.author.email} -> ответ #{self.submission_id}"


# ============================================================
# Общение: форум курса (публично) и личные сообщения (1:1).
#
# Кто с кем (согласовано в чате):
# - Форум привязан к курсу. Участники = активные студенты курса +
#   преподаватели курса. Посторонние форум не видят.
# - Личка - только между студентом и преподавателем, у которых есть
#   ОБЩИЙ курс (студент купил курс, который ведёт этот препод).
#   Студент-студент личку не делаем.
# Хелперы доступа - is_course_participant / can_direct_message ниже.
# ============================================================


class ForumThread(models.Model):
    """ Тема обсуждения на форуме курса. """
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='forum_threads',
        verbose_name='Курс',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='forum_threads',
        verbose_name='Автор',
    )
    title = models.CharField(max_length=255, verbose_name='Заголовок темы')
    is_pinned = models.BooleanField(
        default=False,
        verbose_name='Закреплена',
        help_text='Закреплённые темы показываются вверху (управляет преподаватель)',
    )
    is_locked = models.BooleanField(
        default=False,
        verbose_name='Закрыта',
        help_text='В закрытой теме отвечать могут только преподаватели',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Тема форума'
        verbose_name_plural = 'Темы форума'
        # Сначала закреплённые, потом свежие
        ordering = ['-is_pinned', '-updated_at']

    def __str__(self):
        return f"{self.course.title}: {self.title}"


class ForumPost(models.Model):
    """ Сообщение (ответ) в теме форума. """
    thread = models.ForeignKey(
        ForumThread,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Тема',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='forum_posts',
        verbose_name='Автор',
    )
    content = models.TextField(verbose_name='Текст')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Сообщение форума'
        verbose_name_plural = 'Сообщения форума'
        ordering = ['created_at']

    def __str__(self):
        return f"{self.thread.title} - {self.author_id}"


class DirectMessage(models.Model):
    """
    Личное сообщение 1:1 между студентом и преподавателем.
    Разрешено, только если у отправителя и получателя есть общий курс
    (см. can_direct_message). Диалог = все сообщения между парой.
    """
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages',
        verbose_name='Отправитель',
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_messages',
        verbose_name='Получатель',
    )
    content = models.TextField(verbose_name='Текст')
    is_read = models.BooleanField(default=False, verbose_name='Прочитано получателем')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Личное сообщение'
        verbose_name_plural = 'Личные сообщения'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['sender', 'recipient', 'created_at']),
        ]

    def __str__(self):
        return f"{self.sender_id} -> {self.recipient_id}"


# ============================================================
# Хелперы доступа для общения
# ============================================================

def is_course_participant(user, course):
    """
    Участник форума курса: активный студент (Enrollment) ИЛИ
    преподаватель курса (CourseTeacher). Суперюзер - всегда.
    """
    if not (user and user.is_authenticated):
        return False
    if user.is_superuser:
        return True
    if Enrollment.objects.filter(user=user, course=course, is_active=True).exists():
        return True
    return CourseTeacher.objects.filter(course=course, teacher=user).exists()


def is_course_teacher(user, course):
    """ Преподаватель этого курса (или суперюзер). """
    if not (user and user.is_authenticated):
        return False
    if user.is_superuser:
        return True
    return CourseTeacher.objects.filter(course=course, teacher=user).exists()


def can_direct_message(user_a, user_b):
    """
    Личка разрешена, если у пары есть общий курс в связке
    студент<->преподаватель (в любую сторону):
    a учится на курсе, который ведёт b, ИЛИ b учится на курсе, который
    ведёт a. Курсы берём по активным Enrollment и CourseTeacher.
    """
    if not (user_a and user_b) or user_a == user_b:
        return False
    a_student_courses = set(
        Enrollment.objects.filter(user=user_a, is_active=True).values_list('course_id', flat=True)
    )
    a_teacher_courses = set(
        CourseTeacher.objects.filter(teacher=user_a).values_list('course_id', flat=True)
    )
    b_student_courses = set(
        Enrollment.objects.filter(user=user_b, is_active=True).values_list('course_id', flat=True)
    )
    b_teacher_courses = set(
        CourseTeacher.objects.filter(teacher=user_b).values_list('course_id', flat=True)
    )
    # a студент у b-препода  ИЛИ  b студент у a-препода
    return bool(a_student_courses & b_teacher_courses) or bool(b_student_courses & a_teacher_courses)
