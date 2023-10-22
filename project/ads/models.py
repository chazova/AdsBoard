from django.db import models
from django.contrib.auth.models import User
from embed_video.fields import EmbedVideoField


class Author(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.author.username


class Ad(models.Model):
    CATEGORY = [
        ('tanks', 'Танки'),
        ('healers', 'Хилы'),
        ('dd', 'ДД'),
        ('merchants', 'Торговцы'),
        ('guild_masters', 'Гилдмастеры'),
        ('quest_givers', 'Квестгиверы'),
        ('blacksmiths', 'Кузнецы'),
        ('tanners', 'Кожевники'),
        ('potion_makers', 'Зельевары'),
        ('spell_masters', 'Мастера заклинаний'),
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.CharField(max_length=15, choices=CATEGORY, verbose_name="Категория")
    create_time = models.DateTimeField(auto_now_add=True)
    ad_title = models.CharField(max_length=255, verbose_name="Заголовок")
    ad_text = models.TextField(verbose_name="Текст")
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name="Цена")

    def __str__(self):
        return f'Ad #{self.pk} - Title: {self.ad_title}'

    def filtered_image_set(self):
        return self.image_set.all()

    def filtered_first_image(self):
        return self.image_set.first().image

    def get_absolute_url(self):  # добавим абсолютный путь, чтобы после создания нас перебрасывало на страницу с товаром
        return f'/ads/{self.id}'

class Reply(models.Model):
    STATUS = [
        ('true', 'Принят'),
        ('false', 'Не принят'),
    ]
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, verbose_name="Объявление")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reply_text = models.TextField(verbose_name="Текст")
    create_time = models.DateTimeField(auto_now_add=True)
    is_confirm = models.CharField(max_length=15, choices=STATUS, default='false', verbose_name="Статус")

    def __str__(self):
        return self.reply_text


class Image(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', verbose_name="Изображение")

    def __str__(self):
        return f'Picture #{self.pk} for ad {self.ad}'


class Video(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    embed_video = EmbedVideoField()

    def __str__(self):
        return f'Embed video #{self.pk} for ad {self.ad}'


