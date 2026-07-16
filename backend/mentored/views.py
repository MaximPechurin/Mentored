from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from django.shortcuts import get_object_or_404

from .models import Course, Book, Consultation, Membership, BlogCategory, BlogPost
from .serializers import UserSerializer, CourseSerializer, BookSerializer, ConsultationSerializer, MembershipSerializer, \
    BlogCategorySerializer, BlogPostSerializer


class RegisterView(APIView):
    """Регистрация нового пользователя"""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'message': 'Пользователь успешно создан!'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    """Получить профиль текущего пользователя"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetProductListView(APIView):
    """ APIView для всех товаров """
    permission_classes = [AllowAny]

    def get(self, request):
        courses = Course.objects.filter(is_active=True)
        books = Book.objects.filter(is_active=True)
        consultations = Consultation.objects.filter(is_active=True)
        memberships = Membership.objects.filter(is_active=True)

        data = {
            'courses': CourseSerializer(courses, many=True).data,
            'books': BookSerializer(books, many=True).data,
            'consultations': ConsultationSerializer(consultations, many=True).data,
            'memberships': MembershipSerializer(memberships, many=True).data,
        }
        return Response(data)


class GetProductBySlugView(APIView):
    """
    GET /products/<slug>/
    Универсальный поиск товара по slug среди всех типов.
    """
    permission_classes = [AllowAny]

    def get(self, request, slug):
        # Карта: модель → сериализатор
        product_map = [
            (Course, CourseSerializer),
            (Book, BookSerializer),
            (Consultation, ConsultationSerializer),
            (Membership, MembershipSerializer),
        ]

        for model, serializer_class in product_map:
            try:
                product = model.objects.get(slug=slug, is_active=True)
                serializer = serializer_class(product, context={'request': request})
                return Response(serializer.data)
            except model.DoesNotExist:
                continue

        return Response(
            {'error': 'Товар не найден'},
            status=status.HTTP_404_NOT_FOUND
        )


class GetCourseListView(APIView):
    """
        GET /courses/ — список всех курсов
        POST /courses/ — создать курс (только админ)
    """
    permission_classes = [AllowAny]

    def get(self, request):
        courses = Course.objects.filter(is_active=True)
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not request.user.is_staff:
            return Response(
                {'error': 'Только для администраторов'},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseDetailView(APIView):
    """
        GET /courses/<slug>/ — детально курс
        PUT /courses/<slug>/ — обновить курс (только админ)
        DELETE /courses/<slug>/ — удалить курс (только админ)
    """
    permission_classes = [AllowAny]

    def get_object(self, slug):
        try:
            return Course.objects.get(slug=slug, is_active=True)
        except Course.DoesNotExist:
            return None

    def get(self, request, slug):
        course = self.get_object(slug)
        if not course:
            return Response(
                {'error': 'Курс не найден'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = CourseSerializer(course)
        return Response(serializer.data)

    def put(self, request, slug):
        if not request.user.is_staff:
            return Response(
                {'error': 'Только для администраторов'},
                status=status.HTTP_403_FORBIDDEN
            )
        course = self.get_object(slug)
        if not course:
            return Response(
                {'error': 'Курс не найден'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = CourseSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug):
        if not request.user.is_staff:
            return Response(
                {'error': 'Только для администраторов'},
                status=status.HTTP_403_FORBIDDEN
            )
        course = self.get_object(slug)
        if not course:
            return Response(
                {'error': 'Курс не найден'},
                status=status.HTTP_404_NOT_FOUND
            )
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GetBookListView(APIView):
    """
        GET /books/ — список всех книг
        POST /books/ — создать книгу (только админ)
    """
    permission_classes = [AllowAny]

    def get(self, request):
        books = Book.objects.filter(is_active=True)
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not request.user.is_staff:
            return Response(
                {'error': 'Только для администраторов'},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookDetailView(APIView):
    """
        GET /books/<slug>/ — детально книга
        PUT /books/<slug>/ — обновить книгу (только админ)
        DELETE /books/<slug>/ — удалить книгу (только админ)
    """
    permission_classes = [AllowAny]

    def get_object(self, slug):
        try:
            return Book.objects.get(slug=slug, is_active=True)
        except Book.DoesNotExist:
            return None

    def get(self, request, slug):
        book = self.get_object(slug)
        if not book:
            return Response(
                {'error': 'Книга не найдена'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = BookSerializer(book)
        return Response(serializer.data)

    def put(self, request, slug):
        if not request.user.is_staff:
            return Response(
                {'error': 'Только для администраторов'},
                status=status.HTTP_403_FORBIDDEN
            )
        book = self.get_object(slug)
        if not book:
            return Response(
                {'error': 'Книга не найдена'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug):
        if not request.user.is_staff:
            return Response(
                {'error': 'Только для администраторов'},
                status=status.HTTP_403_FORBIDDEN
            )
        book = self.get_object(slug)
        if not book:
            return Response(
                {'error': 'Книга не найдена'},
                status=status.HTTP_404_NOT_FOUND
            )
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GetConsultationListView(APIView):
    """
        GET /consultations/ — список всех консультаций
        POST /consultations/ — создать консультацию (только админ)
    """
    permission_classes = [AllowAny]

    def get(self, request):
        consultations = Consultation.objects.filter(is_active=True)
        serializer = ConsultationSerializer(consultations, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not request.user.is_staff:
            return Response(
                {'error': 'Только для администраторов'},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = ConsultationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConsultationDetailView(APIView):
    """
        GET /consultations/<slug>/ — детально консультация
        PUT /consultations/<slug>/ — обновить консультацию (только админ)
        DELETE /consultations/<slug>/ — удалить консультацию (только админ)
    """
    permission_classes = [AllowAny]

    def get_object(self, slug):
        try:
            return Consultation.objects.get(slug=slug, is_active=True)
        except Consultation.DoesNotExist:
            return None

    def get(self, request, slug):
        consultation = self.get_object(slug)
        if not consultation:
            return Response(
                {'error': 'Консультация не найдена'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = ConsultationSerializer(consultation)
        return Response(serializer.data)

    def put(self, request, slug):
        if not request.user.is_staff:
            return Response(
                {'error': 'Только для администраторов'},
                status=status.HTTP_403_FORBIDDEN
            )
        consultation = self.get_object(slug)
        if not consultation:
            return Response(
                {'error': 'Консультация не найдена'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = ConsultationSerializer(consultation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug):
        if not request.user.is_staff:
            return Response(
                {'error': 'Только для администраторов'},
                status=status.HTTP_403_FORBIDDEN
            )
        consultation = self.get_object(slug)
        if not consultation:
            return Response(
                {'error': 'Консультация не найдена'},
                status=status.HTTP_404_NOT_FOUND
            )
        consultation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GetMembershipListView(APIView):
    """
        GET /memberships/ — список всех мембершипов
        POST /memberships/ — создать мембершип (только админ)
    """
    permission_classes = [AllowAny]

    def get(self, request):
        memberships = Membership.objects.filter(is_active=True)
        serializer = MembershipSerializer(memberships, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not request.user.is_staff:
            return Response(
                {'error': 'Только для администраторов'},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = MembershipSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MembershipDetailView(APIView):
    """
        GET /memberships/<slug>/ — детально мембершип
        PUT /memberships/<slug>/ — обновить мембершип (только админ)
        DELETE /memberships/<slug>/ — удалить мембершип (только админ)
    """
    permission_classes = [AllowAny]

    def get_object(self, slug):
        try:
            return Membership.objects.get(slug=slug, is_active=True)
        except Membership.DoesNotExist:
            return None

    def get(self, request, slug):
        membership = self.get_object(slug)
        if not membership:
            return Response(
                {'error': 'Мембершип не найден'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = MembershipSerializer(membership)
        return Response(serializer.data)

    def put(self, request, slug):
        if not request.user.is_staff:
            return Response(
                {'error': 'Только для администраторов'},
                status=status.HTTP_403_FORBIDDEN
            )
        membership = self.get_object(slug)
        if not membership:
            return Response(
                {'error': 'Мембершип не найден'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = MembershipSerializer(membership, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug):
        if not request.user.is_staff:
            return Response(
                {'error': 'Только для администраторов'},
                status=status.HTTP_403_FORBIDDEN
            )
        membership = self.get_object(slug)
        if not membership:
            return Response(
                {'error': 'Мембершип не найден'},
                status=status.HTTP_404_NOT_FOUND
            )
        membership.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BlogCategoryListView(APIView):
    """GET /blog/categories/ — список всех категорий"""
    permission_classes = [AllowAny]

    def get(self, request):
        categories = BlogCategory.objects.all()
        serializer = BlogCategorySerializer(categories, many=True)
        return Response(serializer.data)


class BlogPostListView(APIView):
    """
    GET /blog/posts/ — список всех постов
    GET /blog/posts/?category=<slug> — фильтр по категории
    """
    permission_classes = [AllowAny]

    def get(self, request):
        queryset = BlogPost.objects.filter(is_published=True)

        # Фильтр по категории
        category_slug = request.query_params.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        queryset = queryset.select_related('category', 'author')
        serializer = BlogPostSerializer(
            queryset,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)


class BlogPostDetailView(APIView):
    """GET /blog/posts/<slug>/ — детально один пост"""
    permission_classes = [AllowAny]

    def get(self, request, slug):
        post = get_object_or_404(BlogPost, slug=slug, is_published=True)
        serializer = BlogPostSerializer(post, context={'request': request})
        return Response(serializer.data)

