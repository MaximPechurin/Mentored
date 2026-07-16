from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User, BlogCategory, BlogPost, FAQ, Testimonial, Product, Book, Course, Consultation, Membership, \
    Cart, CartItem


class UserSerializer(serializers.ModelSerializer):
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
    class Meta:
        model = CartItem
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'



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