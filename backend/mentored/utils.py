import os
import uuid
from datetime import datetime
from django.utils.encoding import force_str


def get_upload_path(instance, filename):
    """
    Функция сохранения файлов с уникальным UUID и сортировкой по дате.
    Используется как upload_to в моделях.
    """
    # Определяем папку по имени модели
    model_name = instance._meta.model_name

    # Карта: модель → папка
    folder_map = {
        'user': 'avatars',
        'blogpost': 'blog/images',
        'blogpost_file': 'blog/files',
        'book': 'books/images',
        'book_file': 'books/files',
        'course': 'courses/images',
        'consultation': 'consultations/images',
        'membership': 'memberships/images',
        'testimonial': 'testimonials',
    }

    # Определяем поле, для которого вызывается функция
    field_name = 'default'
    for field in instance._meta.get_fields():
        if hasattr(field, 'upload_to') and field.upload_to == get_upload_path:
            field_name = field.name
            break

    # Если поле не найдено, пытаемся определить по типу файла
    if field_name == 'default':
        if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg')):
            field_name = 'images'
        elif filename.lower().endswith(('.pdf', '.epub', '.doc', '.docx', '.txt', '.zip')):
            field_name = 'files'
        else:
            field_name = 'uploads'

    # Получаем папку для модели и поля
    model_folder = folder_map.get(model_name, model_name)
    if field_name in ['images', 'files']:
        # Для blogpost у нас уже есть полный путь
        if model_name == 'blogpost' and field_name == 'images':
            folder = 'blog/images'
        elif model_name == 'blogpost' and field_name == 'files':
            folder = 'blog/files'
        elif model_name == 'book' and field_name == 'files':
            folder = 'books/files'
        else:
            folder = f"{model_folder}/{field_name}"
    else:
        # Для специфичных полей (avatar, book_file, author_image)
        special_map = {
            'avatar': 'avatars',
            'book_file': 'books/files',
            'author_image': 'testimonials',
        }
        folder = special_map.get(field_name, model_folder)

    # Формируем путь
    new_filename = '{folder}/%Y/%m/%d/{uuid}/{file_name}'.format(
        folder=folder,
        uuid=uuid.uuid4(),
        file_name=filename,
    )
    new_filename = force_str(new_filename)
    new_filename = datetime.now().strftime(new_filename)
    new_filename = force_str(new_filename)
    new_filename = os.path.normpath(new_filename)

    return new_filename