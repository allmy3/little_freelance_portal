from django.urls import path

from .views import *

urlpatterns = [
    path('login/', LoginPage.as_view(), name='login'),
    path('logout/', LogoutPage.as_view(), name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),
    path('profile/<username>/', profile, name='profile'),
    path('change-profile-data/', ChangeProfilePage.as_view(), name='change_profile'),
    path('give-rate-to-<username>/', give_rate, name='give_rate'),
    path('password-change/',password_change,name='password_change'),
    path('companies/',CompanyListView.as_view(), name='companies'),
    path('send-response-to-company-<int:pk>/',send_res_com, name='send_res_to_company'),
]