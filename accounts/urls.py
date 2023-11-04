from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.register,name="register"),
    path('login/',views.login,name="login"),
    path('profile/view',views.view,name="profile_view"),
    path('profile/edit',views.edit,name="profile_edit")
]