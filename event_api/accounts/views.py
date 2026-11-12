from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.serializers import UserSerializer

# Create your views here.
class Register(APIView):
    def post(self,request):
        s_ins = UserSerializer(data=request.data)
        if s_ins.is_valid():
            s_ins.save()
            return Response(s_ins.data,status=status.HTTP_201_CREATED)
        else:
            return Response(s_ins.errors,status=status.HTTP_400_BAD_REQUEST)


class LogOut(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print(self, request.user)
        self.request.user.auth_token.delete()
        return Response({"message": "Logout successfully"})