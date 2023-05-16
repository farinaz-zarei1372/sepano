from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from . import token
from .models import Usermodel
from .serializer import SignupUser, LoginUser, ListUser


class SignupAPIView(APIView):

    def post(self, request):
        serializer = SignupUser(data=request.data)
        if serializer.is_valid():
            serializer.save()
            res = {'status': status.HTTP_201_CREATED}
            return Response(res, status=status.HTTP_201_CREATED)
        res = {'status': status.HTTP_400_BAD_REQUEST, 'data': serializer.errors}
        return Response(res, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):

    def post(self, request):
        serializer = LoginUser(data=request.data)
        if serializer.is_valid():
            phonenumber = serializer.validated_data["phonenumber"]
            password = serializer.validated_data["password"]
            username = Usermodel.objects.get(phonenumber=phonenumber).username
            user = authenticate(request, username=username, password=password)
            if user is not None:
                res_data = token.get_tokens_for_user(User.objects.get(username=username))
                response = {
                    "status": status.HTTP_200_OK,
                    "message": "success",
                    "data": res_data
                }
                return Response(response, status=status.HTTP_200_OK)
            else:
                response = {
                    "status": status.HTTP_401_UNAUTHORIZED,
                    "message": "Invalid Phonenumber or Password",
                }
                return Response(response, status=status.HTTP_401_UNAUTHORIZED)
        response = {
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "bad request",
            "data": serializer.errors
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class AccountsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = Usermodel.objects.all()
        serializer = ListUser(data, many=True)
        response = {
            "status": status.HTTP_200_OK,
            "message": "success",
            "data": serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)
