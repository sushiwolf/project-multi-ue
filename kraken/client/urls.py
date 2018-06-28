from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/',  views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('pvc/', views.pvc, name='pvc'),
    path('pvc/<int:problem_id>', views.detail, name='detail'),
    path('pvc/<int:problem_id>/result', views.result, name='result'),
    path('django_view/', views.django_view, name='django_view'),
]
