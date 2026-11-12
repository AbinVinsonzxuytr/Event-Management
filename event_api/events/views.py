from django.shortcuts import get_object_or_404
from rest_framework import serializers
from events.serializer import EventSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from events.permission import IsOrganizer
from events.models import Event


class EventListCreate(APIView):
    permission_classes=[IsOrganizer]

    def get(self,request):
        data=Event.objects.all()
        serializer_instance=EventSerializer(data,many=True)
        return Response(serializer_instance.data)


    def post(self,request):
        serializer_instance=EventSerializer(data=request.data)
        if serializer_instance.is_valid():
            serializer_instance.save(organizer=request.user)
            return Response(serializer_instance.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer_instance.errors,status=status.HTTP_400_BAD_REQUEST)

class RetrieveUpdateDelete(APIView):
    def put(self,request,id):
        data= get_object_or_404(Event, id=id)
        serializer_instance=EventSerializer(data,request.data)
        if serializer_instance.is_valid():
            serializer_instance.save(organizer=request.user)
            return Response(serializer_instance.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer_instance.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            data= Event.objects.get(id=id)
            data.delete()
            return Response({"message": "Deleted successfully"})
        except:
            return Response({"message": " not exist"})