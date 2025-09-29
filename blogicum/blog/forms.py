from django import forms

from .models import Post, Comment, User


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('author',)
        widgets = {
            'pub_date': forms.DateTimeInput(
                format='%Y-%m-%d %H:%M:%S',
                attrs={'type': 'datetime-local'}
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pub_date'].widget = forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'class': 'form-control'  # для Bootstrap стилей
            }
        )


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
