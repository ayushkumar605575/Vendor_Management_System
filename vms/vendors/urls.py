from django.urls import path
from .views import *

urlpatterns = [
    path('vendors/', vendorListCreateView, name='vendor-list-create'),
    path('vendors/<int:pk>/', vendorRetrieveUpdateDeleteView, name='vendor-retrieve-update-delete'),
    path('purchase_orders/', purchaseOrderListCreateView, name='purchase-order-list-create'),
    path('purchase_orders/<int:pk>/', purchaseOrderRetrieveUpdateDeleteView, name='purchase-order-retrieve-update-delete'),
    path('vendors/<int:pk>/performance/', vendorPerformanceView, name='vendor-performance'),
    path('purchase_orders/<int:pk>/acknowledge/', acknowledgePurchaseOrderView, name='acknowledge-purchase-order'),
]