from django.urls import path

from .api_views import (
    CsrfTokenView,
    DashboardSummaryView,
    LoginView,
    LogoutView,
    MeView,
    RegisterView,
)

urlpatterns = [
    path('auth/csrf/', CsrfTokenView.as_view(), name='api_csrf_token'),
    path('auth/register/', RegisterView.as_view(), name='api_register'),
    path('auth/login/', LoginView.as_view(), name='api_login'),
    path('auth/logout/', LogoutView.as_view(), name='api_logout'),
    path('auth/me/', MeView.as_view(), name='api_me'),
    path('dashboard/', DashboardSummaryView.as_view(), name='api_dashboard_summary'),
]
