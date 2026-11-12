from rest_framework import serializers
from booking.models import Booking

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model=Booking
        fields='__all__'
        read_only_fields=['user','status','amount','created_at']

    def validate(self, data):

        seats=data['seats']
        event=data['event']
        if seats>event.available_seats:
            raise serializers.ValidationError("seats not available")
        return data
