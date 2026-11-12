
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from booking.serializer import BookingSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from booking.permission import IsCustomer
from booking.models import Booking
from rest_framework.permissions import IsAuthenticated

from dotenv import load_dotenv

load_dotenv()

import os
api_key=os.getenv("api_key")

class BookingView(APIView):
    permission_classes=[IsCustomer]
    def post(self,request):
        serializer_instance = BookingSerializer(data=request.data)
        if serializer_instance.is_valid():
            data=serializer_instance.validated_data
            event=data['event']
            seats=data['seats']
            amount=event.amount*seats
            u=request.user
            serializer_instance.save(user=u,amount=amount)
            response = {
                "message": """Booking Successfully Created.Payment is Pending,
                make your payment within 15 minutes""",
                "booking_data": serializer_instance.data
            }
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer_instance.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self,request):
        user=request.user
        if user.role=="customer":
            b=Booking.objects.filter(user=request.user)
            serializer_instance=BookingSerializer(b,many=True)
            return Response(serializer_instance.data, status=status.HTTP_200_OK)
        else:
            b=Booking.objects.filter(event__organizer=request.user)
            serializer_instance = BookingSerializer(b, many=True)


        return Response(serializer_instance.data, status=status.HTTP_200_OK)


class RetrieveUpdateDelete(APIView):
    permission_classes=[IsCustomer]
    def put(self,request,id):
        data= get_object_or_404(Bookind,id=id)
        serializer_instance=BookingSerializer(data,request.data)
        if serializer_instance.is_valid():
            data = serializer_instance.validated_data
            event = data['event']
            seats = data['seats']
            amount = event.amount * seats
            u = request.user
            serializer_instance.save(user=u, amount=amount)
            return Response(serializer_instance.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer_instance.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            data= Booking.objects.get(id=id)
            data.delete()
            return Response({"message": "Deleted successfully"})
        except:
            return Response({"message": "Employee not exist"})

class Booking_Cancel(APIView):
    permission_classes=[IsCustomer]
    def get(self,request,id):
        b=get_object_or_404(Booking,id=id)
        b.status="Cancelled"
        b.save()
        return Response({"message":"Booking cancelled Successfully"},status=status.HTTP_200_OK)


# AI-ChatBot Integration

from google import genai
from google.genai import types
from events.models import Event



client=genai.Client(api_key=api_key) #create a client connection using api key

class AIChatbotView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        user_msg=request.data['message']  #fetch user message
        if not user_msg:
            return Response({'message':'user not found'})

        user=request.user
        user_role=user.role
        user_name=user.username

        active_events=Event.objects.filter(available_seats__gt=0)
        print(active_events)
        if active_events:
            event_list=" "
            for e in active_events:
                event_list=f"Title:{e.title},Organizer:{e.organizer.username},Description:{e.description},date:{e.date},time{e.time},Amount:{e.amount},Venue:{e.venue},Available_Seats:{e.available_seats}"
            print(event_list)
            database_context=f"These are the current live events:{event_list}"
        else:
            database_context=f"There are no active events in our Database"

        system_instruction=(
                        f"You are a dedicated AI Assistant for our Event Booking Platform.\n"
                        f"The user speaking to you is '{user_name}' who is a '{user_role}'.\n\n"
                        "STRICT GUIDELINES:\n"
                        "1. ONLY answer questions related to events in our database, ticket prices, seat counts, booking workflows, or event creation support.\n"
                        "2. If the user asks general knowledge questions, coding/math help, general news, or anything UNRELATED to events or our platform, politely reply:\n"
                        "   'ക്ഷമിക്കണം, എനിക്ക് ഈവന്റുകളുമായും ബുക്കിംഗുമായും ബന്ധപ്പെട്ട ചോദ്യങ്ങൾക്ക് മാത്രമേ മറുപടി നൽകാൻ സാധിക്കൂ.' (or equivalent in English if the query is in English).\n"
                        "3. Do NOT make up fake events. Only answer using the live database events provided below.\n\n"
                        f"{database_context}"
        )
        try:
            response=client.models.generate_content(
                model="gemini-3.5-flash",
                contents=user_msg,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,temperature=0.7
                )
            )
            return Response({"message":response.text},status=status.HTTP_200_OK)

        except:
            return Response({"message":"error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)