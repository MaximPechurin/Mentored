from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User, BlogCategory, BlogPost, FAQ, Testimonial, Product, Book, Course, Consultation, Membership, \
    Cart, CartItem, Order, OrderItem


class RegisterSerializer(serializers.ModelSerializer):
    """
    Регистрация нового пользователя.

    Раньше RegisterView использовал UserSerializer(fields='__all__') -
    из-за этого пароль сохранялся как есть, БЕЗ хеширования (ModelSerializer.
    create() просто делает Model.objects.create(**validated_data), не зовёт
    set_password()) - зарегистрированным пользователем невозможно было
    залогиниться (Django сравнивает с хешем, а в базе лежал plain text).
    Заодно '__all__' пускал в тело запроса is_staff/is_superuser/is_active -
    можно было выдать себе права администратора прямо при регистрации.
    Здесь - только безопасный набор полей + пароль хешируется через
    set_password() в create().
    """
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'password', 'confirm_password']

    def validate(self, attrs):
        if attrs['password'] != attrs.pop('confirm_password'):
            raise serializers.ValidationError({'confirm_password': 'Пароли не совпадают'})
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class ProfileSerializer(serializers.ModelSerializer):
    """
    Просмотр/редактирование профиля текущего пользователя.

    Раньше ProfileView использовал тот же дырявый UserSerializer
    (fields='__all__') - GET отдавал во фронт в т.ч. хеш пароля, а PUT
    позволял залогиненному пользователю прописать себе is_staff/is_superuser
    (mass assignment). Здесь - только поля, которые реально нужны профилю;
    пароль и права доступа сюда не попадают вообще (смена пароля - отдельная
    задача с проверкой старого пароля, тут не реализована).
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'avatar', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class UserSerializer(serializers.ModelSerializer):
    """
    ВНИМАНИЕ: fields='__all__' на модели User - НЕ использовать напрямую для
    регистрации/редактирования профиля (утечка хеша пароля, mass assignment
    is_staff/is_superuser). Для этого - RegisterSerializer/ProfileSerializer
    выше. Оставлен только на случай, если где-то нужен полный дамп юзера для
    служебных/админских целей (сейчас нигде в проекте не используется).
    """
    class Meta:
        model = User
        fields = '__all__'


class BlogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = '__all__'


class BlogPostSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = [
            'id',
            'image',
            'title',
            'slug',
            'short_description',
            'content',
            'file',
            'is_published',
            'created_at',
            'updated_at',
            'category',
            'author'
        ]

    def get_category(self, obj):
        """Возвращает название категории"""
        if obj.category:
            return obj.category.name
        return None

    def get_author(self, obj):
        """Возвращает полное имя автора"""
        if obj.author:
            return obj.author.get_full_name() or obj.author.username
        return None


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'


class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class ConsultationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultation
        fields = '__all__'


class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    product_type = serializers.SerializerMethodField()
    product_name = serializers.SerializerMethodField()
    product_price = serializers.SerializerMethodField()
    product_image = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = [
            'id',
            'cart',
            'quantity',
            'product_type',
            'product_name',
            'product_price',
            'product_image',
            'total_price',
            'created_at',
        ]

    def get_product_type(self, obj):
        return obj.content_type.model

    def get_product_name(self, obj):
        if obj.product:
            return obj.product.name
        return None

    def get_product_price(self, obj):
        if obj.product and hasattr(obj.product, 'price'):
            return float(obj.product.price)
        return None

    def get_product_image(self, obj):
        if obj.product and hasattr(obj.product, 'image'):
            request = self.context.get('request')
            if request and obj.product.image:
                return request.build_absolute_uri(obj.product.image.url)
        return None

    def get_total_price(self, obj):
        if obj.product and hasattr(obj.product, 'price'):
            return float(obj.product.price * obj.quantity)
        return 0


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_items = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = [
            'id',
            'user',
            'items',
            'total_items',
            'total_price',
            'created_at',
            'updated_at',
        ]

    def get_total_items(self, obj):
        return obj.total_items

    def get_total_price(self, obj):
        return float(obj.total_price)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'  # 👈 ГЛАВНОЕ!

    def validate(self, attrs):
        # Принудительно используем email для аутентификации
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = User.objects.filter(email=email).first()
            if user and user.check_password(password):
                # Устанавливаем username для JWT
                attrs['username'] = user.username
            else:
                from rest_framework.exceptions import AuthenticationFailed
                raise AuthenticationFailed('No active account found with the given credentials')
        else:
            from rest_framework.exceptions import AuthenticationFailed
            raise AuthenticationFailed('Email and password are required')

        return super().validate(attrs)


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    # related_name='items' на OrderItem.order - без явного объявления DRF его
    # не подставит, и order.items во фронте (OrderPage.vue) всегда был пуст.
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'