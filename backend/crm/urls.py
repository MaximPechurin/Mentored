from django.urls import path

from .views import DashboardView, StudentListView, StudentDetailView, CourseListView, CourseDetailView, CourseStudentsView, \
    CourseOrdersView

app_name = 'crm'

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('students/', StudentListView.as_view(), name='students'),
    path('students/<int:pk>/', StudentDetailView.as_view(), name='student-detail'),
    path('courses/', CourseListView.as_view(), name='courses'),
    path('courses/<int:pk>/', CourseDetailView.as_view(), name='course-detail'),
    path('courses/<int:pk>/students/', CourseStudentsView.as_view(), name='course-students'),
    path('courses/<int:pk>/orders/', CourseOrdersView.as_view(), name='course-orders'),
    # path('teachers/', TeacherListView.as_view(), name='teachers'),
    # path('teachers/<int:pk>/', TeacherDetailView.as_view(), name='teacher-detail'),
    # path('orders/', OrderListView.as_view(), name='orders'),
    # path('orders/<str:order_number>/', OrderDetailView.as_view(), name='order-detail'),
    # path('payments/', PaymentListView.as_view(), name='payments'),
    # path('contact-messages/', ContactMessageListView.as_view(), name='contact-messages'),
    # path('submissions/', SubmissionListView.as_view(), name='submissions'),
]