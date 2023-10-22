from django.forms import ModelForm
from .models import Ad, Reply, Image, Video
from django import forms

# Создаём модельную форму
class AdsForm(ModelForm):
# В класс мета, как обычно, надо написать модель, по которой будет строиться форма, и нужные нам поля. Мы уже делали что-то похожее с фильтрами
    class Meta:
        model = Ad
        fields = ['category', 'ad_title', 'ad_text', 'price']
        widgets = {
            'category': forms.Select(attrs={
                'class': 'form-control',
            }),
            'ad_title': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'ad_text': forms.Textarea(attrs={
                'class': 'form-control',
            }),
            'price': forms.TextInput(attrs={
                'type': 'number',
                'class': 'form-control',
                'value': 0
            }),
        }


class ReplyForm(ModelForm):
# В класс мета, как обычно, надо написать модель, по которой будет строиться форма, и нужные нам поля. Мы уже делали что-то похожее с фильтрами
    class Meta:
        model = Reply
        fields = ['reply_text']
        widgets = {
            'reply_text': forms.Textarea(attrs={
                'class': 'form-control',
            }),
        }

class ImageForm(ModelForm):
    class Meta:

        model = Image
        fields = ['image']

class VideoForm(ModelForm):
    class Meta:

        model = Video
        fields = ['embed_video']


