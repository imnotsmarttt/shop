from django import forms

from .models import ProductComment


class CommentForm(forms.ModelForm):
    """Форма добавления комментария"""
    class Meta:
        model = ProductComment
        fields = ['content']
        labels = {label: '' for label in fields}

        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'comment-input', 'placeholder': 'Введите комментарий'
            }),
        }
