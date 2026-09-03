from django.urls import path

from .views import (
    MyCoursesView, CourseDetailView, LessonProgressView,
    AssignmentDetailView, AssignmentSubmitView, AssignmentAnswersView,
    SubmissionCommentsView, SubmissionVisibilityView,
    TeacherCoursesView, TeacherCourseStudentsView, TeacherStudentCourseDetailView,
    TeacherSubmissionsView, TeacherSubmissionReviewView, TeacherHomeworkView,
    CourseThreadsView, ThreadDetailView, ThreadPostsView, ThreadModerateView,
    ConversationsView, ConversationView, ChatDirectoryView,
    TeacherCourseAnalyticsView, PlatformAnalyticsView,
)

urlpatterns = [
    # Студент
    path('my-courses/', MyCoursesView.as_view(), name='school-my-courses'),
    # str, а не slug - Course.slug генерируется с allow_unicode=True
    # (заголовки на русском/испанском с диакритикой), а встроенный
    # slug-конвертер матчит только ASCII [-a-zA-Z0-9_]+ и 404-тил бы
    # на любом слаге с не-ASCII символом ещё до вызова CourseDetailView.
    path('courses/<str:slug>/', CourseDetailView.as_view(), name='school-course-detail'),
    path('lessons/<int:lesson_id>/progress/', LessonProgressView.as_view(), name='school-lesson-progress'),
    path('assignments/<int:assignment_id>/', AssignmentDetailView.as_view(), name='school-assignment-detail'),
    path('assignments/<int:assignment_id>/submit/', AssignmentSubmitView.as_view(), name='school-assignment-submit'),
    path('assignments/<int:assignment_id>/answers/', AssignmentAnswersView.as_view(), name='school-assignment-answers'),
    path('submissions/<int:submission_id>/comments/', SubmissionCommentsView.as_view(), name='school-submission-comments'),
    path('submissions/<int:submission_id>/visibility/', SubmissionVisibilityView.as_view(), name='school-submission-visibility'),

    # Преподаватель
    path('teacher/courses/', TeacherCoursesView.as_view(), name='school-teacher-courses'),
    path('teacher/courses/<int:course_id>/students/', TeacherCourseStudentsView.as_view(), name='school-teacher-course-students'),
    path('teacher/courses/<int:course_id>/students/<int:user_id>/', TeacherStudentCourseDetailView.as_view(), name='school-teacher-student-course-detail'),
    path('teacher/courses/<int:course_id>/analytics/', TeacherCourseAnalyticsView.as_view(), name='school-teacher-course-analytics'),
    path('teacher/homework/', TeacherHomeworkView.as_view(), name='school-teacher-homework'),
    path('teacher/submissions/', TeacherSubmissionsView.as_view(), name='school-teacher-submissions'),
    path('teacher/submissions/<int:submission_id>/review/', TeacherSubmissionReviewView.as_view(), name='school-teacher-submission-review'),

    # Форум курса
    path('courses/<int:course_id>/threads/', CourseThreadsView.as_view(), name='school-course-threads'),
    path('threads/<int:thread_id>/', ThreadDetailView.as_view(), name='school-thread-detail'),
    path('threads/<int:thread_id>/posts/', ThreadPostsView.as_view(), name='school-thread-posts'),
    path('threads/<int:thread_id>/moderate/', ThreadModerateView.as_view(), name='school-thread-moderate'),

    # Личные сообщения / чат
    path('chat/directory/', ChatDirectoryView.as_view(), name='school-chat-directory'),
    path('messages/', ConversationsView.as_view(), name='school-conversations'),
    path('messages/<int:user_id>/', ConversationView.as_view(), name='school-conversation'),

    # Аналитика
    path('analytics/overview/', PlatformAnalyticsView.as_view(), name='school-analytics-overview'),
]
