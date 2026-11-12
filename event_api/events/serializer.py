from rest_framework import serializers
from events.models import Event
from datetime import datetime

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model=Event
        fields="__all__"
        read_only_fields=['organizer','created_at']

    def validate(self, data):
        date=data['date']
        today_date=datetime.today().date()
        today_date_time=datetime.today().time()
        # month=today().month
        # year=dateTime.today().year
        # day=dateTime.today().day

        if date<today_date:
            raise serializers.ValidationError("Invalid Date")
        return data

