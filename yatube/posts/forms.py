from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    """Форма для создания и редактирования постов"""
    
    class Meta:
        model = Post
        fields = ('text', 'group')
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'group': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'text': 'Текст поста',
            'group': 'Группа (необязательно)',
        }
        help_texts = {
            'text': 'Поделитесь своими мыслями...',
            'group': 'Выберите сообщество для публикации',
        }