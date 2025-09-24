from django.contrib import admin
from django.urls import path
from myapp import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('admin/', admin.site.urls),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path('tender/', views.tender_create, name='tender_list'),
    path('insertuser/', views.insertuser, name='insertuser'),
    path('create/', views.create_task, name='create_task'),
    path('success/', views.task_success, name='task_success'),
    path('registered/', views.registered, name='user_success'),
    path('client/', views.client_create, name='create_client'),
    path("clients/<int:pk>/", views.client_detail, name="client_detail"),
    path("tenders/download/excel/", views.tender_export_excel, name="tender_export_excel"),
    path("tenders/download/pdf/", views.tender_export_pdf, name="tender_export_pdf"),
    path("invoices/", views.invoices_view, name="invoices"),
    path("clients/download/", views.download_clients_csv, name="download_clients_csv"),

]

