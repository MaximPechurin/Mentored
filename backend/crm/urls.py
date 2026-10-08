from django.urls import path

from .views import DashboardView, StudentListView, StudentDetailView, CourseListView, CourseDetailView, CourseStudentsView, \
    CourseOrdersView, TeacherListView, TeacherDetailView, OrderListView, OrderDetailView, PaymentListView, ContactMessageListView, \
    ContactMessageBulkActionView, ContactMessageUnreadCountView, ContactMessageDetailView, SubmissionListView, \
    SubmissionDetailView, SalesReportExportView, StudentExportView, CourseExportView, CourseReportExportView, \
    TeacherExportView, OrderExportView, SubmissionExportView, ContactMessageExportView

app_name = 'crm'

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('students/', StudentListView.as_view(), name='students'),
    path('students/<int:pk>/', StudentDetailView.as_view(), name='student-detail'),
    path('courses/', CourseListView.as_view(), name='courses'),
    path('courses/<int:pk>/', CourseDetailView.as_view(), name='course-detail'),
    path('courses/<int:pk>/students/', CourseStudentsView.as_view(), name='course-students'),
    path('courses/<int:pk>/orders/', CourseOrdersView.as_view(), name='course-orders'),
    path('teachers/', TeacherListView.as_view(), name='teachers'),
    path('teachers/<int:pk>/', TeacherDetailView.as_view(), name='teacher-detail'),
    path('orders/', OrderListView.as_view(), name='orders'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('payments/', PaymentListView.as_view(), name='payments'),
    path('contact-messages/', ContactMessageListView.as_view(), name='contact-messages'),
    path('contact-messages/bulk/', ContactMessageBulkActionView.as_view(), name='contact-messages-bulk'),
    path('contact-messages/unread-count/', ContactMessageUnreadCountView.as_view(), name='contact-messages-unread-count'),
    path('contact-messages/<int:pk>/', ContactMessageDetailView.as_view(), name='contact-message-detail'),
    path('submissions/', SubmissionListView.as_view(), name='submissions'),
    path('submissions/<int:pk>/', SubmissionDetailView.as_view(), name='submission-detail'),
    path('reports/sales/', SalesReportExportView.as_view(), name='sales-report-export'),
    path('students/export/', StudentExportView.as_view(), name='students-export'),
    path('courses/export/', CourseExportView.as_view(), name='courses-export'),
    path('courses/<int:pk>/report/', CourseReportExportView.as_view(), name='course-report-export'),
    path('teachers/export/', TeacherExportView.as_view(), name='teachers-export'),
    path('orders/export/', OrderExportView.as_view(), name='orders-export'),
    path('submissions/export/', SubmissionExportView.as_view(), name='submissions-export'),
    path('contact-messages/export/', ContactMessageExportView.as_view(), name='contact-messages-export'),
]