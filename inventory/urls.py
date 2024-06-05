from django.urls import path
from .views import InventoryItemListCreateAPIView, InventoryItemDetailAPIView, SupplierListCreateAPIView, SupplierDetailAPIView

urlpatterns = [
    path('inventory/', InventoryItemListCreateAPIView.as_view(), name='inventory-list-create'),
    path('inventory/<int:pk>/', InventoryItemDetailAPIView.as_view(), name='inventory-detail'),
    path('suppliers/', SupplierListCreateAPIView.as_view(), name='supplier-list-create'),
    path('suppliers/<int:pk>/', SupplierDetailAPIView.as_view(), name='supplier-detail'),
]
