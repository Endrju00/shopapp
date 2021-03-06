from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'items'
urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<int:sale_id>/', views.detail, name='detail'),
    path('filtered/<str:filter>/', views.filter, name='filter'),
    path('item/', views.add_item, name='add_item'),
    path('create/', views.create_sale, name='add_sale'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
