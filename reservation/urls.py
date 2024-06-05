from django.urls import path
from .views import RoomTypeView, RoomView, RoomEditView, ReservationListCreateView, ReservationDetailView, InvoiceDetailView, InvoiceListView

urlpatterns = [
    path('room-type/',RoomTypeView.as_view({'get':'list','post':'create'})),
    path('room-type/<int:pk>/',RoomTypeView.as_view({'get':'retrieve','put':'update','delete':'destroy'})),
    path('room/',RoomView.as_view()),
    path('room/<int:pk>/',RoomEditView.as_view()),
    path('reservations/',ReservationListCreateView.as_view(), name='reservation-list-create'),
    path('reservations/<int:pk>/',ReservationDetailView.as_view(), name='reservation-detail'),
    path('invoices/', InvoiceListView.as_view(), name='invoice-list'),
    path('invoices/<int:pk>/',InvoiceDetailView.as_view(), name='invoice-detail')
]