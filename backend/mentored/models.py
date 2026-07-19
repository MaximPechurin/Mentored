from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from .utils import get_upload_path



# ============================================
# 1. Пользователь и всё что с ним связано
# ============================================

class User(AbstractUser):
    """ Расширенная модель пользователя """

    email = models.EmailField(
        unique=True,
        verbose_name='Email'
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Номер телефона'
    )
    avatar = models.ImageField(
        upload_to=get_upload_path,
        blank=True,
        null=True,
        verbose_name='Аватар'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='mentored_user_set',
        blank=True,
        verbose_name='Группы'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='mentored_user_set',
        blank=True,
        verbose_name='Права доступа'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-id']

    def __str__(self):
        return self.email or self.username

# ============================================
# 2. Блог и всё что с ним связано
# ============================================

class BlogCategory(models.Model):
    """ Категории для постов блога """
    name = models.CharField(
        max_length=100,
        verbose_name='Название'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Слаг'
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядок'
    )

    class Meta:
        verbose_name = 'Категория блога'
        verbose_name_plural = 'Категории блога'

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    """ Пост в блоге """

    category = models.ForeignKey(
        BlogCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts',
        verbose_name='Категория'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='blog_posts',
        verbose_name='Автор (может быть пустым)'
    )
    image = models.ImageField(
        upload_to=get_upload_path,
        blank=True,
        null=True,
        verbose_name='Изображение'
    )
    title = models.CharField(
        max_length=255,
        verbose_name='Наименование'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Слаг (для красивой ссылки, формируется автоматически)'
    )
    short_description = models.CharField(
        max_length=500,
        verbose_name='Краткое описание'
    )
    content = models.TextField(
        verbose_name='Полное описание'
    )
    file = models.FileField(
        upload_to=get_upload_path,
        blank=True,
        null=True,
        verbose_name='Файл'
    ) # Файл (может быть PDF, аудио, видео и т.д.)
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

# ============================================
# 3. Часто задаваемые вопросы и всё что с ними связано
# ============================================

class FAQ(models.Model):
    """ Часто задаваемые вопросы """

    question = models.CharField(
        max_length=500,
        verbose_name='Вопрос'
    )
    answer = models.TextField(
        verbose_name='Ответ'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активен'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    class Meta:
        verbose_name = 'Часто задаваемый вопрос'
        verbose_name_plural = 'Часто задаваемые вопросы'
        ordering = ['id']

    def __str__(self):
        return self.question

# ============================================
# 4. Модель отзывов и всё что с ними связано
# ============================================

class Testimonial(models.Model):
    """ Отзывы клиентов """

    text = models.TextField(
        verbose_name='Текст отзыва'
    )
    author = models.CharField(
        max_length=100,
        verbose_name='Имя автора'
    )
    author_role = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Роль/Должность'
    )
    author_initial = models.CharField(
        max_length=2,
        blank=True,
        null=True,
        verbose_name='Инициалы'
    )
    author_image = models.ImageField(
        upload_to=get_upload_path,
        blank=True,
        null=True,
        verbose_name='Фото автора'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активен'
    )
    is_featured = models.BooleanField(
        default=False,
        verbose_name='Рекомендуемый'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.author}: {self.text[:50]}..."

# ============================================
# 5. Абстрактная модель Продукта и её модели
# ============================================

# ============================================================
# АБСТРАКТНАЯ МОДЕЛЬ PRODUCT
# ============================================================
class Product(models.Model):
    """
    Абстрактная базовая модель для всех товаров.
    """
    name = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='Слаг')
    short_description = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name='Краткое описание'
    )
    description = models.TextField(verbose_name='Полное описание')
    long_description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Длинное описание'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена'
    )
    old_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name='Старая цена'
    )
    image = models.ImageField(
        upload_to='',  # Будет переопределён в дочерних моделях
        blank=True,
        null=True,
        verbose_name='Изображение'
    )
    includes = models.TextField(
        blank=True,
        null=True,
        verbose_name='Что входит',
        help_text='Каждый пункт с новой строки'
    )
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    is_featured = models.BooleanField(default=False, verbose_name='Рекомендуемый')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        abstract = True
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @property
    def has_discount(self):
        return self.old_price and self.old_price > 0

    @property
    def discount_percent(self):
        if self.has_discount:
            return int((self.old_price - self.price) / self.old_price * 100)
        return 0

    def get_includes_list(self):
        if not self.includes:
            return []
        return [item.strip() for item in self.includes.split('\n') if item.strip()]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


# ============================================================
# КНИГА
# ============================================================
class Book(Product):
    image = models.ImageField(
        upload_to=get_upload_path,
        blank=True,
        null=True,
        verbose_name='Изображение'
    )
    book_format = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Формат книги'
    )
    pages = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name='Количество страниц'
    )
    book_language = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Язык книги'
    )
    year = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name='Год издания'
    )
    book_file = models.FileField(
        upload_to=get_upload_path,
        blank=True,
        null=True,
        verbose_name='Файл книги'
    )
    acceso = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Доступ'
    )

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

    def __str__(self):
        return f"Книга: {self.name}"


# ============================================================
# КУРС
# ============================================================
class Course(Product):
    image = models.ImageField(
        upload_to=get_upload_path,
        blank=True,
        null=True,
        verbose_name='Изображение'
    )
    duration = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Длительность курса'
    )
    lessons = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name='Количество уроков'
    )
    video_hours = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Часов видео'
    )
    level = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Уровень'
    )
    certificate = models.BooleanField(
        default=False,
        verbose_name='Есть сертификат'
    )
    format_course = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Формат'
    )
    acceso = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Доступ'
    )

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    def __str__(self):
        return f"Курс: {self.name}"


# ============================================================
# КОНСУЛЬТАЦИЯ
# ============================================================
class Consultation(Product):
    image = models.ImageField(
        upload_to=get_upload_path,
        blank=True,
        null=True,
        verbose_name='Изображение'
    )
    duration_minutes = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name='Длительность (минуты)'
    )
    expert = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Эксперт'
    )
    platform = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Платформа'
    )
    languages = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Языки (через запятую)'
    )
    format_consultation = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Формат'
    )
    agenda = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Повестка дня'
    )

    class Meta:
        verbose_name = 'Консультация'
        verbose_name_plural = 'Консультации'

    def __str__(self):
        return f"Консультация: {self.name}"


# ============================================================
# МЕМБЕРШИП
# ============================================================
class Membership(Product):
    image = models.ImageField(
        upload_to=get_upload_path,
        blank=True,
        null=True,
        verbose_name='Изображение'
    )
    cycle = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Период (месячный, годовой)'
    )
    cancel_anytime = models.BooleanField(
        default=True,
        verbose_name='Можно отменить в любое время'
    )
    format_membership = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Формат'
    )
    permanencia = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Постоянство (для вывода в membership)'
    )

    class Meta:
        verbose_name = 'Мембершип'
        verbose_name_plural = 'Мембершипы'

    def __str__(self):
        return f"Мембершип: {self.name}"


# ============================================
# 6. Корзина и айтемы корзины
# ============================================

class Cart(models.Model):
    """
    Корзина пользователя.
    У одного пользователя может быть только одна активная корзина.
    """
    user = models.OneToOneField(
        'User',
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Пользователь'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return f"Корзина {self.user.email or self.user.username}"

    @property
    def total_items(self):
        """Общее количество товаров в корзине"""
        return self.items.aggregate(models.Sum('quantity'))['quantity__sum'] or 0

    @property
    def total_price(self):
        """Общая сумма корзины"""
        total = 0
        for item in self.items.all():
            total += item.total_price
        return total


class CartItem(models.Model):
    """
    Элемент корзины: конкретный товар с количеством.
    """
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Корзина'
    )

    # GenericForeignKey для связи с разными моделями товаров
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        verbose_name='Тип товара'
    )
    object_id = models.PositiveIntegerField(
        verbose_name='ID товара'
    )
    product = GenericForeignKey('content_type', 'object_id')

    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name='Количество'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    class Meta:
        verbose_name = 'Элемент корзины'
        verbose_name_plural = 'Элементы корзины'
        # Чтобы не было дублей: один и тот же товар не может быть дважды
        unique_together = ('cart', 'content_type', 'object_id')

    def __str__(self):
        return f"{self.quantity}x {self.product} в корзине {self.cart.user.email}"

    @property
    def total_price(self):
        """Стоимость позиции = цена товара × количество"""
        if hasattr(self.product, 'price'):
            return self.product.price * self.quantity
        return 0


# ============================================
# 7. Модель заказа
# ============================================

class Order(models.Model):
    """ Основная модель заказа """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='Пользователь'
    )
    cart = models.OneToOneField(
        Cart,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='order',
        verbose_name='Корзина'
    )
    #payment = models.OneToOneField(
    #    'payments.Payment',
    #    on_delete=models.SET_NULL,
    #    null=True,
    #    blank=True,
    #    related_name='order',
    #    verbose_name='Платёж'
    #)
    order_number = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Номер заказа'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Статус'
    )
    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Сумма без налогов'
    )
    tax = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name='Налоги'
    )
    shipping = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name='Доставка'
    )
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Итоговая сумма'
    )

    is_digital = models.BooleanField(
        default=False,
        verbose_name='Цифровой заказ (без доставки)'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paid_at = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self.generate_order_number()
        super().save(*args, **kwargs)

    def generate_order_number(self):
        import random
        import string
        from django.utils import timezone
        prefix = 'ORD'
        timestamp = timezone.now().strftime('%Y%m%d')
        random_part = ''.join(random.choices(string.digits, k=6))
        return f"{prefix}-{timestamp}-{random_part}"


# ============================================================
# ЭЛЕМЕНТ ЗАКАЗА (OrderItem)
# ============================================================
class OrderItem(models.Model):
    """
    Элемент заказа — товары, которые были куплены.
    Хранит замороженную информацию на момент покупки.
    """
    order = models.ForeignKey(
        'Order',
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Заказ'
    )
    # === СВЯЗЬ С ТОВАРОМ ===
    product_type = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Тип товара (course, book, consultation, membership)'
    )
    product_id = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name='ID товара'
    )
    # === ЗАМОРОЖЕННЫЕ ДАННЫЕ ===
    product_name = models.CharField(
        max_length=255,
        verbose_name='Название товара'
    )
    product_sku = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Артикул'
    )
    product_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена товара'
    )
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name='Количество'
    )
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Итоговая сумма'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    class Meta:
        verbose_name = 'Элемент заказа'
        verbose_name_plural = 'Элементы заказа'
        ordering = ['id']

    def __str__(self):
        return f"{self.quantity}x {self.product_name} (Заказ #{self.order.order_number})"

    def save(self, *args, **kwargs):
        if not self.total:
            self.total = self.product_price * self.quantity
        super().save(*args, **kwargs)