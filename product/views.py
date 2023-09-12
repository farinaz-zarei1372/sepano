from rest_framework import routers
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Product
from .serializer import ProductSerializer


class ProductViewset(viewsets.ViewSet):

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def createproduct(self, request):
        if not request.user.is_shop_owner:
            res = {'message': 'you dont have permission to add product', 'status': status.HTTP_403_FORBIDDEN}
            return Response(res, status=status.HTTP_403_FORBIDDEN)
        serializer = ProductSerializer(data=request.data)
        if not serializer.is_valid():
            res = {'status': status.HTTP_400_BAD_REQUEST, 'data': serializer.errors}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        res = {'status': status.HTTP_201_CREATED}
        return Response(res, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['delete'], permission_classes=[IsAuthenticated])
    def deleteproduct(self, request):
        if not request.user.is_shop_owner:
            res = {'message': 'you dont have permission to delete product', 'status': status.HTTP_403_FORBIDDEN}
            return Response(res, status=status.HTTP_403_FORBIDDEN)
        serializer = ProductSerializer(data=request.data, partial=True)
        if not serializer.is_valid():
            res = {'status': status.HTTP_400_BAD_REQUEST, 'data': serializer.errors}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        deleted_product = Product.objects.filter(id=request.data['id']).first()
        if deleted_product is not None:
            deleted_product.delete()
            res = {'status': status.HTTP_200_OK}
            return Response(res, status=status.HTTP_200_OK)
        else:
            response = {
                "status": status.HTTP_404_NOT_FOUND,
                "message": "queryset not found",
                "data": serializer.errors
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated])
    def editproduct(self, request, pk):
        if not request.user.is_shop_owner:
            res = {'message': 'you dont have permission to edit product', 'status': status.HTTP_403_FORBIDDEN}
            return Response(res, status=status.HTTP_403_FORBIDDEN)
        serializer = ProductSerializer(data=request.data, partial=True)
        if not serializer.is_valid():
            res = {'status': status.HTTP_400_BAD_REQUEST, 'data': serializer.errors}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)

        edited_product: Product = Product.objects.get(id=pk)
        if edited_product is not None:
            if request.data.get('name'):
                edited_product.name = request.data.get('name')
            if request.data.get('inventory'):
                edited_product.inventory = request.data.get('inventory')
            if request.data.get('price'):
                edited_product.price = request.data.get('price')
            if request.data.get('image'):
                edited_product.image = request.data.get('image')
            edited_product.save(update_fields=['name', 'inventory', 'price', 'image'])

            response = {
                "status": status.HTTP_205_RESET_CONTENT,
                "message": "success",
                # "data": serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = {
                "status": status.HTTP_404_NOT_FOUND,
                "message": "queryset not found",
                "data": serializer.errors
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def listproduct(self, request):
        router = routers.SimpleRouter()
        router.register(r'product', ProductViewset, basename='product')
        data = Product.objects.all()
        serializer = ProductSerializer(data, many=True)
        response = {
            "status": status.HTTP_200_OK,
            "message": "success",
            "data": serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)

# ------------------------------------------------------------------------------------
# class ProductAPIView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request):
#         if not request.user.is_shop_owner:
#             res = {'message': 'you have not permission to add product', 'status': status.HTTP_403_FORBIDDEN}
#             return Response(res, status=status.HTTP_403_FORBIDDEN)
#         serializer = ProductSerializer(data=request.data)
#         if not serializer.is_valid():
#             res = {'status': status.HTTP_400_BAD_REQUEST, 'data': serializer.errors}
#             return Response(res, status=status.HTTP_400_BAD_REQUEST)
#         serializer.save()
#         res = {'status': status.HTTP_201_CREATED}
#         return Response(res, status=status.HTTP_201_CREATED)
#
#
# class DeleteProductAPIView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request, name):
#         if not request.user.is_shop_owner:
#             res = {'message': 'you have not permission to delete product', 'status': status.HTTP_403_FORBIDDEN}
#             return Response(res, status=status.HTTP_403_FORBIDDEN)
#         serializer = DeleteProductSerializer(data=request.data)
#         if not serializer.is_valid():
#             res = {'status': status.HTTP_400_BAD_REQUEST, 'data': serializer.errors}
#             return Response(res, status=status.HTTP_400_BAD_REQUEST)
#
#         deleted_product = Product.objects.filter(name=name)
#         deleted_product.delete()
#         res = {'status': status.HTTP_200_OK}
#         return Response(res, status=status.HTTP_200_OK)
#
#
# class EditProductAPIView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request, name):
#         if not request.user.is_shop_owner:
#             res = {'message': 'you have not permission to edit product', 'status': status.HTTP_403_FORBIDDEN}
#             return Response(res, status=status.HTTP_403_FORBIDDEN)
#         serializer = ProductSerializer(data=request.data)
#         if not serializer.is_valid():
#             res = {'status': status.HTTP_400_BAD_REQUEST, 'data': serializer.errors}
#             return Response(res, status=status.HTTP_400_BAD_REQUEST)
#
#         edited_product: Product = Product.objects.get(name=name)
#         if edited_product is not None:
#             if request.GET.get('name'):
#                 edited_product.name = request.GET.get('name')
#             if request.GET.get('inventory'):
#                 edited_product.inventory = request.GET.get('inventory')
#             if request.GET.get('price'):
#                 edited_product.price = request.GET.get('price')
#             if request.GET.get('image'):
#                 edited_product.image = request.GET.get('image')
#
#             edited_product.save()
#             # serializer = ProductSerializer(edited_product, many=True)
#
#             response = {
#                 "status": status.HTTP_205_RESET_CONTENT,
#                 "message": "success",
#                 # "data": serializer.data
#             }
#             return Response(response, status=status.HTTP_200_OK)
#         else:
#             response = {
#                 "status": status.HTTP_404_NOT_FOUND,
#                 "message": "queryset not found",
#                 "data": serializer.errors
#             }
#             return Response(response, status=status.HTTP_404_NOT_FOUND)
#
#
# class ProductlistAPIView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request):
#         data = Product.objects.all()
#         serializer = ProductSerializer(data, many=True)
#         response = {
#             "status": status.HTTP_200_OK,
#             "message": "success",
#             "data": serializer.data
#         }
#         return Response(response, status=status.HTTP_200_OK)
#
# # Create your views here.
