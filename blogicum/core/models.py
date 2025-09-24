from django.db import models


class PublishedModel(models.Model):
    """Абстрактная базовая модель с полями is_published и created_at."""

    is_published = models.BooleanField(default=True,
                                       verbose_name='Опубликовано',
                                       help_text='Снимите галочку, '
                                       'чтобы скрыть публикацию.')
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Добавлено')

    class Meta:
        abstract = True


class Clearpublished(models.Model):
    """Базовая абстрактная модель без help_text"""

    is_published = models.BooleanField(default=True,
                                       verbose_name='Опубликовано')
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Добавлено')

    class Meta:
        abstract = True
