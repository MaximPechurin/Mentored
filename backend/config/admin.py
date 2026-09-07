"""
Кастомный AdminSite: группирует модели приложений `mentored` (витрина,
заказы, блог) и `school` (учебная платформа) в осмысленные блоки на
главной странице админки - по умолчанию Django валит все модели
приложения в один длинный список. Модель Payment (приложение `payments`)
по смыслу относится к заказам - визуально подмешиваем её в блок
«Заказы и оплата» сайта. Приложение `auth` (группы Django) не трогаем -
отображается как обычно.
"""
from django.contrib.admin import AdminSite

# Разбивка моделей school по блокам. Ключ object_name в нижнем регистре.
SCHOOL_SECTIONS = [
    ("🎓 Школа · Работа с курсами", [
        "course", "module", "lesson", "lessonmaterial",
        "assignment", "courseteacher", "productcourseaccess",
    ]),
    ("👤 Школа · Студенты и доступы", [
        "enrollment", "lessonprogress", "submission", "submissioncomment",
        "certificate", "teacherprofile",
    ]),
    ("💬 Школа · Общение", [
        "forumthread", "forumpost", "directmessage",
    ]),
]

# Разбивка моделей mentored (+ Payment из приложения payments) по блокам.
MENTORED_SECTIONS = [
    ("🛍️ Сайт · Витрина (товары)", [
        "book", "course", "consultation", "membership",
    ]),
    ("🧾 Сайт · Заказы и оплата", [
        "cart", "cartitem", "order", "payment",
    ]),
    ("📝 Сайт · Контент", [
        "blogcategory", "blogpost", "faq", "testimonial",
    ]),
    ("👤 Сайт · Пользователи и роли", [
        "role", "user",
    ]),
    ("✉️ Сайт · Обращения", [
        "contactmessage",
    ]),
    ("⚙️ Сайт · Настройки", [
        "sitesettings",
    ]),
]


def _grouped_sections(models_by_name, sections, leftover_title, app_label, app_url):
    """ Раскладывает модели по секциям; то, что не попало ни в одну - в «Прочее». """
    result = []
    placed = set()
    for title, names in sections:
        models = [models_by_name[n] for n in names if n in models_by_name]
        placed.update(n for n in names if n in models_by_name)
        if models:
            result.append({
                "name": title,
                "app_label": app_label,
                "app_url": app_url,
                "has_module_perms": True,
                "models": models,
            })

    leftover = [m for n, m in models_by_name.items() if n not in placed]
    if leftover:
        result.append({
            "name": leftover_title,
            "app_label": app_label,
            "app_url": app_url,
            "has_module_perms": True,
            "models": leftover,
        })
    return result


class MentoredAdminSite(AdminSite):
    site_header = "Mentored — администрирование"
    site_title = "Mentored admin"
    index_title = "Панель управления"
    # Главная с гайдом (school/templates/admin/guia_index.html)
    index_template = "admin/guia_index.html"

    def get_app_list(self, request, app_label=None):
        app_list = super().get_app_list(request, app_label)

        school_app = next((a for a in app_list if a.get("app_label") == "school"), None)
        mentored_app = next((a for a in app_list if a.get("app_label") == "mentored"), None)
        payments_app = next((a for a in app_list if a.get("app_label") == "payments"), None)
        other = [a for a in app_list if a not in (school_app, mentored_app, payments_app)]

        school_sections = []
        if school_app:
            by_name = {m["object_name"].lower(): m for m in school_app["models"]}
            school_sections = _grouped_sections(
                by_name, SCHOOL_SECTIONS, "🎓 Школа · Прочее",
                "school", school_app.get("app_url", "/admin/school/"),
            )

        mentored_sections = []
        if mentored_app:
            by_name = {m["object_name"].lower(): m for m in mentored_app["models"]}
            if payments_app:
                # Payment визуально живёт в блоке заказов сайта, хотя
                # физически это отдельное приложение payments
                by_name.update({m["object_name"].lower(): m for m in payments_app["models"]})
            mentored_sections = _grouped_sections(
                by_name, MENTORED_SECTIONS, "🛍️ Сайт · Прочее",
                "mentored", mentored_app.get("app_url", "/admin/mentored/"),
            )

        # Сайт (магазин), затем школа, затем всё остальное (auth и т.п.)
        return mentored_sections + school_sections + other
