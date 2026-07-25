from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType

from .models import Course, Book, Consultation, Membership, BlogCategory, BlogPost, Cart, CartItem, Order, FAQ, OrderItem
from .serializers import RegisterSerializer, ProfileSerializer, CourseSerializer, BookSerializer, ConsultationSerializer, MembershipSerializer, \
    BlogCategorySerializer, BlogPostSerializer, CartSerializer, CartItemSerializer, OrderSerializer, FAQSerializer


class RegisterView(APIView):
    """Регистрация нового пользователя"""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
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
        serializer = ProfileSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        serializer = ProfileSerializer(user, data=request.data, partial=True)
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

class CartView(APIView):
    """GET /cart/ — получить текущую корзину пользователя"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart, context={'request': request})
        return Response(serializer.data)


class CartAddItemView(APIView):
    """POST /cart/add/ — добавить товар в корзину"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_type = request.data.get('product_type')
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)

        if not product_type or not product_id:
            return Response(
                {'error': 'product_type и product_id обязательны'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Маппинг типов
        model_map = {
            'course': Course,
            'book': Book,
            'consultation': Consultation,
            'membership': Membership,
        }

        model = model_map.get(product_type)
        if not model:
            return Response(
                {'error': f'Неизвестный тип товара: {product_type}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            product = model.objects.get(id=product_id, is_active=True)
        except model.DoesNotExist:
            return Response(
                {'error': 'Товар не найден'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Получаем или создаём корзину
        cart, _ = Cart.objects.get_or_create(user=request.user)

        # Получаем ContentType для товара
        content_type = ContentType.objects.get_for_model(model)

        # Ищем существующий элемент
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            content_type=content_type,
            object_id=product_id,
            defaults={'quantity': quantity}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        serializer = CartItemSerializer(cart_item, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CartUpdateItemView(APIView):
    """PUT /cart/update/<item_id>/ — обновить количество товара"""
    permission_classes = [IsAuthenticated]

    def put(self, request, item_id):
        try:
            cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
        except CartItem.DoesNotExist:
            return Response(
                {'error': 'Товар не найден в корзине'},
                status=status.HTTP_404_NOT_FOUND
            )

        quantity = request.data.get('quantity')
        if quantity is None or quantity < 0:
            return Response(
                {'error': 'quantity должно быть >= 0'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if quantity == 0:
            cart_item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        cart_item.quantity = quantity
        cart_item.save()
        serializer = CartItemSerializer(cart_item, context={'request': request})
        return Response(serializer.data)


class CartRemoveItemView(APIView):
    """DELETE /cart/remove/<item_id>/ — удалить товар из корзины"""
    permission_classes = [IsAuthenticated]

    def delete(self, request, item_id):
        try:
            cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
        except CartItem.DoesNotExist:
            return Response(
                {'error': 'Товар не найден в корзине'},
                status=status.HTTP_404_NOT_FOUND
            )

        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CartClearView(APIView):
    """DELETE /cart/clear/ — очистить корзину"""
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        CartItem.objects.filter(cart__user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CreateOrderView(APIView):
    """POST /orders/create/ — создать заказ из активной корзины"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart = Cart.objects.filter(user=request.user).first()
        if not cart or cart.items.count() == 0:
            return Response(
                {'error': 'Корзина пуста'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Создаём заказ
        total = cart.total_price
        #tax = subtotal * 0.1  # 10%
        #shipping = 0  # для цифровых товаров
        #total = subtotal + tax + shipping

        order = Order.objects.create(
            user=request.user,
            cart=cart,
            #subtotal=subtotal,
            #tax=tax,
            #shipping=shipping,
            total=total,
            is_digital=True,
            is_active=True,
            status='pending',
        )

        # Переносим товары из корзины в OrderItem
        for cart_item in cart.items.all():
            product = cart_item.product
            OrderItem.objects.create(
                order=order,
                product_type=cart_item.content_type.model,
                product_id=cart_item.object_id,
                product_name=product.name,
                product_price=product.price,
                quantity=cart_item.quantity,
                total=product.price * cart_item.quantity,
                #is_digital=True,
            )

        # Очищаем корзину (но сохраняем ссылку в заказе)
        cart.items.all().delete()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderHistoryView(APIView):
    """GET /orders/ — получить историю заказов пользователя"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


class OrderDetailView(APIView):
    """GET /orders/<order_number>/ — детали заказа"""
    permission_classes = [IsAuthenticated]

    def get(self, request, order_number):
        order = get_object_or_404(Order, order_number=order_number, user=request.user)
        serializer = OrderSerializer(order)
        return Response(serializer.data)


class FAQView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        faq = FAQ.objects.filter(is_active=True)
        serializer = FAQSerializer(faq, many=True)
        return Response(serializer.data)


class GetOrderByNumberView(APIView):
    """GET /orders/<order_number>/ — получить заказ по номеру"""
    permission_classes = [IsAuthenticated]

    def get(self, request, order_number):
        try:
            order = Order.objects.get(order_number=order_number, user=request.user)
        except Order.DoesNotExist:
            return Response(
                {'error': 'Заказ не найден'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = OrderSerializer(order)
        return Response(serializer.data)