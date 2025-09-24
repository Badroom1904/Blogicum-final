from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.core.paginator import Paginator
from django.views.generic import DeleteView
from django import forms
from django.contrib.messages.views import SuccessMessageMixin
from .models import Post, Category, Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder':
                                          'Введите ваш комментарий...'}),
        }


class IndexView(ListView):
    """Главная страница - 10 последних опубликованных постов с пагинацией"""

    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.select_related('category').filter(
            pub_date__lte=timezone.now(),
            is_published=True,
            category__is_published=True
        ).order_by('-pub_date')


class PostDetailView(DetailView):
    """Страница отдельной публикации"""

    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get_queryset(self):
        return Post.objects.select_related('category').filter(
            pub_date__lte=timezone.now(),
            is_published=True,
            category__is_published=True
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = self.object.comments.all()
        return context


class CategoryPostsView(ListView):
    """Страница категории с пагинацией"""

    template_name = 'blog/category.html'
    context_object_name = 'post_list'
    paginate_by = 10  # Добавляем пагинацию

    def get_queryset(self):
        category = get_object_or_404(Category,
                                     slug=self.kwargs
                                     ['category_slug'], is_published=True)
        return Post.objects.filter(
            category=category,
            is_published=True,
            pub_date__lte=timezone.now()
        ).select_related('location').order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(
            Category, slug=self.kwargs['category_slug'], is_published=True)
        return context


class UserRegistrationView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/registration_form.html'
    success_url = reverse_lazy('login')


class ProfileView(DetailView):
    """Страница профиля пользователя"""

    model = User
    template_name = 'blog/profile.html'
    context_object_name = 'profile'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object

        posts = Post.objects.filter(author=user).select_related(
            'category', 'location').order_by('-pub_date')

        if self.request.user != user:
            posts = posts.filter(
                is_published=True,
                pub_date__lte=timezone.now(),
                category__is_published=True
            )

        # Добавляем пагинацию (10 постов на страницу)
        paginator = Paginator(posts, 10)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['page_obj'] = page_obj
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    """Создание нового поста"""

    model = Post
    template_name = 'blog/create.html'
    fields = ['title', 'text', 'pub_date', 'category', 'location', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:profile', kwargs={'username':
                                               self.request.user.username})


class ProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """Редактирование профиля пользователя"""

    model = User
    template_name = 'blog/user.html'  # Используем существующий шаблон
    fields = ['first_name', 'last_name', 'username', 'email']
    success_message = "Профиль успешно обновлен"

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('blog:profile', kwargs={'username':
                                               self.request.user.username})


class CommentCreateView(LoginRequiredMixin, CreateView):
    """Добавление комментария"""

    form_class = CommentForm
    template_name = 'blog/detail.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk':
                                                   self.kwargs['post_id']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        context['post'] = post
        context['comments'] = post.comments.all()
        return context


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование комментария"""

    form_class = CommentForm  # Используем нашу форму
    template_name = 'blog/comment.html'

    def get_queryset(self):
        return Comment.objects.filter(author=self.request.user)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.object.post.pk})


class PostUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование публикации"""

    model = Post
    template_name = 'blog/create.html'
    fields = ['title', 'text', 'pub_date', 'category', 'location', 'image']

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.object.pk})


class PostDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление публикации"""

    model = Post
    template_name = 'blog/create.html'
    context_object_name = 'post'

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

    def get_success_url(self):
        return reverse('blog:profile', kwargs={'username':
                                               self.request.user.username})


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление комментария"""

    model = Comment
    template_name = 'blog/comment.html'

    def get_queryset(self):
        return Comment.objects.filter(author=self.request.user)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.object.post.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = self.object.post
        return context


class CustomPasswordChangeView(PasswordChangeView):
    """Кастомная страница смены пароля"""

    template_name = 'registration/password_change_form.html'
    success_url = reverse_lazy('blog:password_change_done')
