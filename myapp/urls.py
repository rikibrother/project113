"""
URL configuration for project113 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
# from django.contrib import admin
# from django.urls import path
# from .import views


# urlpatterns = [
#     path('',views.homepage, name='homepage'),
#     path('',views.login, name='login'),
#     path('',views.admin, name='admin'),
    
# ]


from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView)
from . import api


urlpatterns = [
    path('', views.homepage, name='homepage'),  
    path('mylogin/', views.mylogin, name='mylogin'), 
    path('admin_panel/', views.admin_panel, name='admin_panel'),  
    path('data/', views.data, name='data'),
    path('formdata/', views.formdata, name='formdata'),
    path('movieform/', views.movie_form, name="movieform"),
    path('moviedata/', views.movie_data, name="moviedata"),
    path('api/user/', api.UserAPI.as_view()),
    path("api/logout/", api.logout),
    path('updatemoviedata/<int:id>/', views.update_movie_data, name="updatemoviedata"),
 
    # added id but teacher not added
    path('delete/<int:id>', views.delete_std, name='delete'),  
    path('update/<int:id>', views.update_std, name='update'),
    path('mylogout/', views.mylogout, name='mylogout'),
    path('signup/', views.signup, name='signup'),
    path('activation/<str:id>/', views.activation, name='activation'),
    path('reset', PasswordResetView.as_view(template_name='pass_reset.html'), name='password_reset'),
    path('password_reset/done', PasswordResetDoneView.as_view(template_name='pass_done.html'), name='password_reset_done'),
    path('password_confirm/<uidb64>/<token>', PasswordResetConfirmView.as_view(template_name='pass_confirm.html'), name='password_reset_confirm'),
    path('password_complete/', PasswordResetCompleteView.as_view(template_name='pass_complete.html'), name='password_reset_complete'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
