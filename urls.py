

from . import views
from django.urls import path,include



urlpatterns = [

    path('', views.home, name="home"),
    path('login/',views.login,name="login"),
    path('register/', views.register, name="register"),
    path('logout/', views.logout, name="logout"),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('patient/', views.patient, name="patient"),
        path('doctor/', views.doctor, name="doctor"),

    path('draft_list/', views.draft_list, name='draft_list'),
    path('viewblog',views.viewblog,name='viewblog'),
    path('addblog',views.addblog,name='addblog'),

]
