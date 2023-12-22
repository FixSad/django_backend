"""
URL configuration for NewDjangoProj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, reverse_lazy
from test_django import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('info/', views.show_info, name='info'),
    path('info/<int:id_user>/edit', views.edit_mechanic, name='edit_mechanic'),
    path('info/messages/', views.show_messages, name='show_messages'),
    path('info/messages/<int:message_id>/accept', views.accept_car, name='accept_car'),
    path('', views.show_index, name='signup'),
    path('showclient/<int:id_user>/', views.show_client),
    path('showclient/<int:id_user>/edit/', views.edit_client, name='edit_client'),
    path('showclient/<int:id_user>/addcar/', views.create_car, name='create_car'),
    path('info/carinfo/<int:car_id>/', views.car_info, name='car_info'),
    path('info/carinfo/<int:car_id>/status/', views.change_car_status, name='change_car_status'),
    path('info/carinfo/<int:car_id>/delete/', views.delete_car, name='delete_car'),
    path('signin/', views.show_sign_in, name='signin'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('signup')), name='logout'),
    path('ajax/validate_username_email', views.validate_username_email, name='validate_username_email'),
    path('ajax/validate_mileage', views.validate_mileage, name='validate_mileage'),
]










