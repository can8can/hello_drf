from django.shortcuts import render

from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveAPIView, CreateAPIView, ListCreateAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, \
    DestroyModelMixin
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ViewSet

from utils.response import APIResponse
from app1.models import Book
from .serializers import BookModelSerializer


class BookAPIView(APIView):
    def get(self,request,*args,**kwargs):
        book_obj_all=Book.objects.all()
        serializer=BookModelSerializer(book_obj_all,many=True).data
        return APIResponse(results=serializer)

class BookGenericAPIView(ListModelMixin,
                         RetrieveModelMixin,
                         CreateModelMixin,
                         UpdateModelMixin,
                         DestroyModelMixin,
                         GenericAPIView):
    queryset = Book.objects.filter(is_delete=False)
    serializer_class = BookModelSerializer
    lookup_field = "id"
    '''
        def get(self,request,*args,**kwargs):
            #book_obj_all=Book.objects.filter(is_delete=False)
            book_obj_all=self.get_queryset()

            #serializer=BookModelSerializer(book_obj_all,many=True).data
            bo_get_ser=self.get_serializer(book_obj_all,many=True).data
            return APIResponse(results=bo_get_ser)
    '''

    def get(self,request,*args,**kwargs):
        if "id" in kwargs:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    #删除
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    # 修改
    def put(self, request, *args, **kwargs):
        response = self.update(request, *args, **kwargs)
        return APIResponse(results=response.data)

    #添加
    def post(self, request, *args, **kwargs):
        create = self.create(request, *args, **kwargs)
        return APIResponse(results=create.data, data_message="增加成功")


    #局部修改
    def patch(self, request, *args, **kwargs):
        response = self.partial_update(request, *args, **kwargs)
        return APIResponse(results=response.data)



class BookGenericMixinView(RetrieveAPIView,ListAPIView, CreateAPIView,DestroyModelMixin,UpdateModelMixin,ListCreateAPIView):
    queryset = Book.objects.filter(is_delete=False)
    serializer_class = BookModelSerializer
    lookup_field = "id"



class BookModelViewSet(ModelViewSet):
    queryset = Book.objects.filter(is_delete=False)
    serializer_class = BookModelSerializer
    lookup_field = "id"

    """定义登录操作"""

    def denglu(self, request, *args, **kwargs):
        # 可以再此方法中完成用户登录
        request_data = request.data
        print(request_data)
        return self.list(request, *args, **kwargs)

    def count(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)







