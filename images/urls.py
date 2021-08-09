from django.urls import path
from .views import create_image, image_detail, image_like, list_images, image_ranking

app_name = 'images'

urlpatterns = [
    path('', list_images, name='image-list'),
    path('most-viewed/', image_ranking, name='image-ranking'),
    path('create-image/', create_image, name='create-image'),
    path('image-detail/<slug:slug>/', image_detail, name='image-detail'),
    path('like/', image_like, name='like'),
]
