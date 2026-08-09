from django.urls import path

from .views import (
    MyCoursesView, CourseDetailView, LessonProgressView,
    AssignmentDetailView, AssignmentSubmitView,
    TeacherSubmissionsView, TeacherSubmissionReviewView,
)

urlpatterns = [
    # Студент
    path('my-courses/', MyCoursesView.as_view(), name='school-my-courses'),
    path('courses/<slug:slug>/', CourseDetailView.as_view(), name='school-course-detail'),
    path('lessons/<int:lesson_id>/progress/', LessonProgressView.as_view(), name='school-lesson-progress'),
    path('assignments/<int:assignment_id>/', AssignmentDetailView.as_view(), name='school-assignment-detail'),
    path('assignments/<int:assignment_id>/submit/', AssignmentSubmitView.as_view(), name='school-assignment-submit'),

    # Преподаватель
    path('teacher/submissions/', TeacherSubmissionsView.as_view(), name='school-teacher-submissions'),
    path('teacher/submissions/<int:submission_id>/review/', TeacherSubmissionReviewView.as_view(), name='school-teacher-submission-review'),
]
