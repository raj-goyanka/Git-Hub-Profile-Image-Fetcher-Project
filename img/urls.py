from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('user_signup/', views.user_signup, name='user_signup'),
    path('user_signin/',  views.user_signin, name='user_signin'),
    path('user_signout/', views.user_signout, name='user_signout'),
    path('images/', views.images, name='images'),
    path('',views.home,name='home'),
    path('deleteimg/<str:name>/',views.deleteimg,name="deleteimg"),
    path('account_verify/<slug:token>/',views.account_verify,name='account_verify'),
    path('userquary/',views.userquary,name="userquary"),
]