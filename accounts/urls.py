from django.contrib.auth import logout
from django.urls import path
# from .views import login_view
from .views import register_view, editprofile, profile_detailview, profile_listview, follow_user
from django.contrib.auth.views import (
    LoginView, 
    LogoutView, 
    PasswordChangeView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView

)



urlpatterns = [
    path('users/', profile_listview, name='profile_list'),
    path('user/<username>/', profile_detailview, name='profile_detail'),
    path('users/follow/', follow_user, name='follow_user'),
    path('edit/', editprofile, name='edit-profile'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', register_view, name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password_change/', PasswordChangeView.as_view(), name='password-change'),
    path('password_reset_view/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

]
