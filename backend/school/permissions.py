from rest_framework.permissions import BasePermission


class IsDev(BasePermission):
    """
    Временный feature-gate: раздел «Школа» уже задеплоен на прод, но
    открыт только пользователям с галкой User.is_dev (и суперюзерам,
    чтобы админ не залочил сам себя). Для обычных пользователей раздел
    закрыт и на фронте, и здесь, в API - недостаточно спрятать кнопки,
    иначе URL можно угадать и дёрнуть API напрямую.

    Когда школу откроют для всех - этот класс снимается со school-вью
    (см. school/views.py), поле is_dev при этом можно оставить.
    """
    message = 'Раздел пока доступен только для разработчиков.'

    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and (user.is_dev or user.is_superuser))


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
