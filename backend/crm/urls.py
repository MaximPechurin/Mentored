from django.urls import path

from .views import DashboardView, StudentListView, StudentDetailView, CourseListView, CourseDetailView, CourseStudentsView, \
    CourseOrdersView, TeacherListView, TeacherDetailView, OrderListView, OrderDetailView, PaymentListView, ContactMessageListView, \
    ContactMessageBulkActionView, ContactMessageUnreadCountView, ContactMessageDetailView, SubmissionListView, \
    SubmissionDetailView, SalesReportExportView, StudentExportView, CourseExportView, CourseReportExportView, \
    TeacherExportView, OrderExportView, SubmissionExportView, ContactMessageExportView

app_name = 'crm'

urlpatterns = [
    # --- Dashboard ---
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    # --- Alumnos ---
    path('students/', StudentListView.as_view(), name='students'),
    path('students/export/', StudentExportView.as_view(), name='students-export'),
    path('students/<int:pk>/', StudentDetailView.as_view(), name='student-detail'),

    # --- Cursos ---
    path('courses/', CourseListView.as_view(), name='courses'),
    path('courses/export/', CourseExportView.as_view(), name='courses-export'),
    path('courses/<int:pk>/report/', CourseReportExportView.as_view(), name='course-report-export'),
    path('courses/<int:pk>/students/', CourseStudentsView.as_view(), name='course-students'),
    path('courses/<int:pk>/orders/', CourseOrdersView.as_view(), name='course-orders'),
    path('courses/<int:pk>/', CourseDetailView.as_view(), name='course-detail'),

    # --- Profesores ---
    path('teachers/', TeacherListView.as_view(), name='teachers'),
    path('teachers/export/', TeacherExportView.as_view(), name='teachers-export'),
    path('teachers/<int:pk>/', TeacherDetailView.as_view(), name='teacher-detail'),

    # --- Pedidos ---
    path('orders/', OrderListView.as_view(), name='orders'),
    path('orders/export/', OrderExportView.as_view(), name='orders-export'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),

    # --- Pagos (оставляем для совместимости, но страница убрана из UI) ---
    path('payments/', PaymentListView.as_view(), name='payments'),

    # --- Mensajes ---
    path('contact-messages/', ContactMessageListView.as_view(), name='contact-messages'),
    path('contact-messages/export/', ContactMessageExportView.as_view(), name='contact-messages-export'),
    path('contact-messages/bulk/', ContactMessageBulkActionView.as_view(), name='contact-messages-bulk'),
    path('contact-messages/unread-count/', ContactMessageUnreadCountView.as_view(), name='contact-messages-unread-count'),
    path('contact-messages/<int:pk>/', ContactMessageDetailView.as_view(), name='contact-message-detail'),

    # --- Tareas ---
    path('submissions/', SubmissionListView.as_view(), name='submissions'),
    path('submissions/export/', SubmissionExportView.as_view(), name='submissions-export'),
    path('submissions/<int:pk>/', SubmissionDetailView.as_view(), name='submission-detail'),

    # --- Отчёты ---
    path('reports/sales/', SalesReportExportView.as_view(), name='sales-report-export'),
]
