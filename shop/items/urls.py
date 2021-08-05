from django.urls import path

from . import views

app_name = 'items'
urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<int:sale_id>/', views.detail, name='detail'),
]
