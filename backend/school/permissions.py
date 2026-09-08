from rest_framework.permissions import BasePermission


class IsStudent(BasePermission):
    """
    Доступ только пользователям с ролью student (см. mentored.Role,
    User.is_student). Не путать с проверкой доступа к конкретному курсу -
    это делает Enrollment, см. school/views.py.
    """
    message = 'Доступно только студентам.'

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_student)


class IsTeacher(BasePermission):
    """
    Доступ только пользователям с ролью teacher (см. mentored.Role,
    User.is_teacher). Не проверяет, что это преподаватель именно этого
    курса - за это отвечает CourseTeacher, проверяется отдельно там,
    где это важно (например, при проверке домашних заданий).
    """
    message = 'Доступно только преподавателям.'

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_teacher)
