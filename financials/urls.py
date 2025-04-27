from django.urls import path
from .import views

urlpatterns = [
    path('', views.home, name='home'),
    path('financials/<str:symbol>/', views.financials_view, name='financials'),
     path('financials/', views.financials_view, name='financials'),  # Notice: no <symbol> here
    
]