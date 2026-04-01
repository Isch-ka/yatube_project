from django import forms
from django.core.exceptions import ValidationError
from .models import Post


def validate_not_empty(value):
    """Проверяет, что поле не пустое и не состоит из одних пробелов"""
    if not value or value.strip() == '':
        raise ValidationError('Поле не может быть пустым!')


class PostForm(forms.ModelForm):
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
    
    def clean_text(self):
        """Валидация поля text"""
        data = self.cleaned_data['text']
        if not data or data.strip() == '':
            raise ValidationError('Текст поста не может быть пустым или состоять только из пробелов!')
        return data