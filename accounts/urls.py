from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path("personal-details/", views.personal_details_view, name="personal_details"),
    path("change-password/", views.change_password_view, name="change_password"),
    path("delete-account/", views.delete_account_view, name="delete_account"),
]
