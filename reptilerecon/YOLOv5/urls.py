from django.urls import path

from . import views

app_name = 'YOLOv5'
urlpatterns = [
    path('', views.UploadVideoFormView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/delete/', views.DeleteView.as_view(), name='delete'),
]
