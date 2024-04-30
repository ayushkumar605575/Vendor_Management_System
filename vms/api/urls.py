from django.urls import path

from . import views

urlpatterns = [
    path('admin/', views),
    path('purchase_orders/', views),
    path('vendors/', views), # GET POST
    path('vendors/<int:id>/', views), # PUT GET DELETE
]