
import debug_toolbar
from accounts.views import dashboard
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from accounts.views import *
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.views import PasswordChangeDoneView, PasswordResetCompleteView

urlpatterns = [
    path('', dashboard, name='home'),
    path('accounts/', include('accounts.urls')),
    path('images/', include('images.urls', namespace='images')),
    path('admin/', admin.site.urls),

    # path('custom-login/', login_view, name='custom-login'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password_change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('__debug__/', include(debug_toolbar.urls))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
