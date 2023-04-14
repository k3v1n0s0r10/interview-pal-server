from django.urls import path

from . import views

urlpatterns = [
    path('register/',
         views.UserViewSet.as_view({'post': 'register'}), name='user-register'),
    path('login/',
         views.UserViewSet.as_view({'post': 'login'}), name='user-login'),
]
