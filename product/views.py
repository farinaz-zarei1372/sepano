from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Products
from .serializer import ProductSerializer


class ProductAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            res = {'status': status.HTTP_201_CREATED}
            return Response(res, status=status.HTTP_201_CREATED)
        res = {'status': status.HTTP_400_BAD_REQUEST, 'data': serializer.errors}
        return Response(res, status=status.HTTP_400_BAD_REQUEST)


class ProductlistAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = Products.objects.all()
        serializer = ProductSerializer(data, many=True)
        response = {
            "status": status.HTTP_200_OK,
            "message": "success",
            "data": serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)

# Create your views here.
