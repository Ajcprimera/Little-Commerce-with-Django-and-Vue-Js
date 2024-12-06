from rest_framework import routers
from .views import ProductViewSet, ReviewViewSet
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()

from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, ReviewViewSet, TagViewSet
from django.urls import path

router = DefaultRouter()

# Registrar ViewSets
router.register('products', ProductViewSet, basename='products')
router.register('tags', TagViewSet, basename='tags')

# Rutas para las reseñas relacionadas con productos
urlpatterns = [
    path('products/<int:product_pk>/reviews/', ReviewViewSet.as_view({'get': 'list', 'post': 'create'}), name='product-reviews'),
    path('products/<int:product_pk>/reviews/<int:pk>/', ReviewViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='product-review-detail'),
]

# Incluir rutas del router
urlpatterns += router.urls
