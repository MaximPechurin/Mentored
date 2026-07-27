from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from .views import GetProductListView, GetCourseListView, CourseDetailView, GetBookListView, BookDetailView, \
    GetConsultationListView, ConsultationDetailView, GetMembershipListView, MembershipDetailView, RegisterView, \
    ProfileView, GetProductBySlugView, BlogPostListView, BlogPostDetailView, CartView, CartAddItemView, \
    CartUpdateItemView, CartRemoveItemView, CartClearView, CreateOrderView, GetOrderByNumberView, OrderHistoryView, ContactMessageView


urlpatterns = [
    # JWT
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # Регистрация и профиль
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),

    # Все товары
    path('products/', GetProductListView.as_view(), name='product-list'),
    path('products/<slug:slug>/', GetProductBySlugView.as_view(), name='product-detail'),

    #Блог и посты
    path('blog/posts/', BlogPostListView.as_view(), name='blog-posts'),
    path('blog/posts/<slug:slug>/', BlogPostDetailView.as_view(), name='blog-post-detail'),

    # ===== КОРЗИНА =====
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/add/', CartAddItemView.as_view(), name='cart-add'),
    path('cart/update/<int:item_id>/', CartUpdateItemView.as_view(), name='cart-update'),
    path('cart/remove/<int:item_id>/', CartRemoveItemView.as_view(), name='cart-remove'),
    path('cart/clear/', CartClearView.as_view(), name='cart-clear'),

    # Заказ
    path('create_order/', CreateOrderView.as_view(), name='create-order'),

    # Контакты
    path('contact/', ContactMessageView.as_view(), name='contact'),
    path('orders/', OrderHistoryView.as_view(), name='order-list'),
    path('orders/<str:order_number>/', GetOrderByNumberView.as_view(), name='order-detail'),

    # Курсы
    #path('courses/', GetCourseListView.as_view(), name='course-list'),
    #path('courses/<slug:slug>/', CourseDetailView.as_view(), name='course-detail'),
    #
    # Книги
    #path('books/', GetBookListView.as_view(), name='book-list'),
    #path('books/<slug:slug>/', BookDetailView.as_view(), name='book-detail'),
    #
    # Консультации
    #path('consultations/', GetConsultationListView.as_view(), name='consultation-list'),
    #path('consultations/<slug:slug>/', ConsultationDetailView.as_view(), name='consultation-detail'),
    #
    # Мембершипы
    #path('memberships/', GetMembershipListView.as_view(), name='membership-list'),
    #path('memberships/<slug:slug>/', MembershipDetailView.as_view(), name='membership-detail'),
]