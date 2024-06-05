from rest_framework import serializers
from .models import RoomType, Room, Reservation, Invoice

class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = '__all__'

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


class ReservationSerializer(serializers.ModelSerializer):
    check_in_date = serializers.DateField(input_formats=['%Y-%m-%d'])
    check_out_date = serializers.DateField(input_formats=['%Y-%m-%d'])
    class Meta:
        model = Reservation
        fields = ['id', 'user', 'room', 'check_in_date', 'check_out_date', 'is_active']
        extra_kwargs = {
            'user': {'error_messages': {'required': 'User field is required.'}},
            'room': {'error_messages': {'required': 'Room field is required.'}},
            'check_in_date': {'error_messages': {'required': 'Check-in date field is required.'}},
            'check_out_date': {'error_messages': {'required': 'Check-out date field is required.'}},
        }
    def validate(self, data):
        required_fields = ['user', 'room', 'check_in_date', 'check_out_date']
        for field in required_fields:
            if field not in data:
                raise serializers.ValidationError({field: ["This field is required."]})

        existing_reservations = Reservation.objects.filter(
            room=data['room'],
            check_out_date__gte=data['check_in_date'],
            check_in_date__lte=data['check_out_date'],
            is_active=True
        ).exclude(id=self.instance.id if self.instance else None)  

        if existing_reservations.exists():
            raise serializers.ValidationError("This room is already reserved for the selected dates.")
        return data

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ['id', 'reservation', 'total_amount', 'created_at']

