from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import GenericAPIView
from .models import RoomType, Room, Reservation, Invoice
from .serializers import RoomTypeSerializer, RoomSerializer, ReservationSerializer, InvoiceSerializer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from .permissions import CustomModelPermission
from rest_framework import generics, status
from datetime import datetime

# Create your views here.
class RoomTypeView(ModelViewSet):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer 
    permission_classes = [AllowAny, CustomModelPermission]  

class RoomView(GenericAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [AllowAny, CustomModelPermission]  

    def get(self,request):
        room_objs =  Room.objects.all()
        serializer = RoomSerializer(room_objs,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class RoomEditView(GenericAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get(self,request,pk):
        try:
            room_obj = Room.objects.get(id=pk)
        except:
            return Response('Data not found!')
        serializer = RoomSerializer(room_obj)
        return Response(serializer.data)
    
    def put(self,request,pk):
        try:
            room_obj = Room.objects.get(id=pk)
        except:
            return Response('Data not found!')
        serializer = RoomSerializer(room_obj,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
    def delete(self,request,pk):
        try:
            room_obj = Room.objects.get(id=pk)
        except:
            return Response('Data not found!')
        room_obj.delete()
        return Response('Data deleted')
    
class ReservationListCreateView(generics.ListCreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated, CustomModelPermission]

    def create(self, request):
        data = request.data.copy()
        required_fields = ['room', 'check_in_date', 'check_out_date', 'user']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            errors = {field: ["This field is required."] for field in missing_fields}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        room_id = data.get('room')
        check_in_date = data.get('check_in_date')
        check_out_date = data.get('check_out_date')
        try:
            room_price = Room.objects.get(pk=room_id).price
        except Room.DoesNotExist:
            return Response({"error": "Invalid room ID."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            check_in_date = datetime.strptime(check_in_date, '%Y-%m-%d').date()
            check_out_date = datetime.strptime(check_out_date, '%Y-%m-%d').date()
        except ValueError:
            return Response({"error": "Invalid date format. Date format should be YYYY-MM-DD."},
                            status=status.HTTP_400_BAD_REQUEST)

        duration = ((check_out_date - check_in_date).days ) + 1
        total_amount = room_price * duration

        reservation_data = {
            'room': room_id,
            'check_in_date': check_in_date,
            'check_out_date': check_out_date,
            'user': request.user.id
        }

        reservation_serializer = ReservationSerializer(data=reservation_data)
        if reservation_serializer.is_valid():
            reservation = reservation_serializer.save()
            invoice_data = {
                'reservation': reservation.id,
                'total_amount': total_amount
            }
            invoice_serializer = InvoiceSerializer(data=invoice_data)
            if invoice_serializer.is_valid():
                invoice_serializer.save()
                return Response(reservation_serializer.data, status=status.HTTP_201_CREATED)
            else:
                reservation.delete() 
                return Response(invoice_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(reservation_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReservationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated, CustomModelPermission]

class InvoiceListView(generics.ListAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated, CustomModelPermission]
    
class InvoiceDetailView(generics.RetrieveAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated, CustomModelPermission]
