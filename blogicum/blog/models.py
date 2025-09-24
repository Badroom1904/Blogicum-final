from django.db import models
from core.models import PublishedModel, Clearpublished
# Импортируем встроенную модель пользователя
from django.contrib.auth import get_user_model
User = get_user_model()
MAX_LENGTH = 256


class Category(PublishedModel):
    """Модель для представления тематической категории публикаций."""

    title = models.CharField(max_length=MAX_LENGTH, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(unique=True, verbose_name='Идентификатор',
                            help_text='Идентификатор страницы для URL; '
                            'разрешены символы латиницы, цифры, дефис'
                            ' и подчёркивание.')

    class Meta:
        """Метаданные модели Category."""

        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Location(Clearpublished):
    """Модель для представления географического местоположения публикации."""

    name = models.CharField(max_length=MAX_LENGTH,
                            verbose_name='Название места')

    class Meta:
        """Метаданные модели Location."""

        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name


class Post(PublishedModel):
    """Модель для представления публикации (поста) в блоге."""

    title = models.CharField(max_length=MAX_LENGTH, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(verbose_name='Дата и время публикации',
                                    help_text='Если установить дату и время '
                                    'в будущем'
                                    ' — можно делать отложенные публикации.')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
        related_name='posts'

    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Местоположение'
    )
    image = models.ImageField(
        'Изображения',
        upload_to = 'posts_image/',
        blank = True,
        null = True
    )

    class Meta:
        """Метаданные модели Post."""

        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return self.title

class Comment(models.Model):
    """Модель для комментариев к публикациям."""
    
    text = models.TextField('Текст комментария')
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Публикация'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор комментария'
    )
    created_at = models.DateTimeField('Дата и время создания комментария', auto_now_add=True)

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['created_at']  # Сортировка по времени (старые → новые)

    def __str__(self):
        return f'Комментарий {self.author} к посту {self.post.id}'