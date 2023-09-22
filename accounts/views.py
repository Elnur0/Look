from django.shortcuts import render
from rest_framework import generics
from django.contrib.auth import get_user_model
from rest_framework.response import Response

from django.utils.encoding import smart_str, smart_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .serializer import LoginSerializer, RegisterSerializer, ActivationSerializer


User = get_user_model()

class LoginView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = LoginSerializer



class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer



class ActivationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = ActivationSerializer
    lookup_field = "uuid"


    def get_object(self, *args, **kwargs):
        uuid = self.kwargs.get("uuid")
        id = smart_str(urlsafe_base64_decode(uuid))
        return User.objects.get(id=id)
    
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"user": self.get_object()})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)