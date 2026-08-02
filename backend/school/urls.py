from django.urls import path

from .views import MyCoursesView, CourseDetailView, LessonProgressView

urlpatterns = [
    path('my-courses/', MyCoursesView.as_view(), name='school-my-courses'),
    path('courses/<slug:slug>/', CourseDetailView.as_view(), name='school-course-detail'),
    path('lessons/<int:lesson_id>/progress/', LessonProgressView.as_view(), name='school-lesson-progress'),
]
