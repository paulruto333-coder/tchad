from django.urls import path
from . import views

urlpatterns = [
    path("", views.network_dashboard, name="landing_page"),  # Home page is now dashboard
    path("dashboard/", views.network_dashboard, name="network_dashboard"),
    path("plans/", views.landing_page, name="plans_page"),  # Plans moved to /plans/
    path("payment/<int:order_id>/", views.ecocash_entry, name="ecocash_entry"),
    path("verify-otp/<int:order_id>/", views.otp_verification, name="otp_verification"),
    path("success/<int:order_id>/", views.success_page, name="success_page"),
    path("records/", views.all_applications, name="all_applications"),
    
    # Authentication URLs
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),
]
