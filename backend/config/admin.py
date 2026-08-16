"""
Кастомный AdminSite: группирует модели приложения `school` в осмысленные
блоки на главной админки (по умолчанию Django валит все модели приложения
в один длинный список). Остальные приложения (mentored, payments, auth)
не трогаем - отображаются как обычно.
"""
from django.contrib.admin import AdminSite

# Разбивка моделей school по блокам. Ключ object_name в нижнем регистре.
SCHOOL_SECTIONS = [
    ("🎓 Школа · Работа с курсами", [
        "course", "module", "lesson", "lessonmaterial",
        "assignment", "courseteacher", "productcourseaccess",
    ]),
    ("👤 Школа · Студенты и доступы", [
        "enrollment", "lessonprogress", "submission", "teacherprofile",
    ]),
    ("💬 Школа · Общение", [
        "forumthread", "forumpost", "directmessage",
    ]),
]


class MentoredAdminSite(AdminSite):
    site_header = "Mentored — администрирование"
    site_title = "Mentored admin"
    index_title = "Панель управления"
    # Главная с гайдом (school/templates/admin/guia_index.html)
    index_template = "admin/guia_index.html"

    def get_app_list(self, request, app_label=None):
        app_list = super().get_app_list(request, app_label)

        # Вытаскиваем приложение school, чтобы разбить его на блоки
        school_app = next((a for a in app_list if a.get("app_label") == "school"), None)
        if not school_app:
            return app_list

        by_name = {m["object_name"].lower(): m for m in school_app["models"]}
        other = list(app_list)
        other.remove(school_app)

        sections = []
        placed = set()
        for title, names in SCHOOL_SECTIONS:
            models = [by_name[n] for n in names if n in by_name]
            placed.update(n for n in names if n in by_name)
            if models:
                sections.append({
                    "name": title,
                    "app_label": "school",
                    "app_url": school_app.get("app_url", "/admin/school/"),
                    "has_module_perms": True,
                    "models": models,
                })

        # Модели school, не попавшие ни в один блок - в отдельный «Прочее»
        leftover = [m for n, m in by_name.items() if n not in placed]
        if leftover:
            sections.append({
                "name": "🎓 Школа · Прочее",
                "app_label": "school",
                "app_url": school_app.get("app_url", "/admin/school/"),
                "has_module_perms": True,
                "models": leftover,
            })

        # Блоки школы - первыми, затем остальные приложения
        return sections + other
