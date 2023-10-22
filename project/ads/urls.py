from django.urls import path

from .views import *

app_name = 'ads'

urlpatterns = [
    path('', AdList.as_view(), name='ads'),
    path('<int:pk>/', AdDetailView.as_view(), name='ad_detail'), # Ссылка на детали товара
    path('add/', AdCreateView.as_view(), name='ad_create'), # Ссылка на создание товара
    path('<int:pk>/edit/', AdUpdateView.as_view(), name='ad_update'), # Ссылка на редактирование товара
    path('<int:pk>/delete/', AdDeleteView.as_view(), name='ad_delete'), # Ссылка на удаление товара
    path('reply_create/<int:ad_id>/', ReplyCreateView.as_view(), name='reply_create'),
    path('user_ads/', UserAdsList.as_view(), name='user_ads'),
    path('replies/', ReplyList.as_view(), name='replies'),
    path('confirm_reply/<int:reply_id>/', confirm_reply, name='confirm_reply'),
    path('delete_reply/<int:reply_id>/', delete_reply, name='delete_reply'),
    path('image_add/<int:ad_id>/', upload_image, name='image_add'),
    path('video_add/<int:ad_id>/', upload_video, name='video_add'),
]