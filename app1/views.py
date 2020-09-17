from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from utils.response import APIResponse
from rest_framework.views import APIView
from app1.models import Book
from .serializers import BookModelSerializer,BookModelDeSerializer,BookModelSerializerV2


class BookAPIView(APIView):
    def get(self,request,*args,**kwargs):
        book_id=kwargs.get("id")
        if book_id:
            book_bj=Book.objects.get(pk=book_id)
            data=BookModelSerializer(book_bj).data
            return Response({
                "status":200,
                "message":"查询成功",
                "results": data
            })
        else:
            book_list_all=Book.objects.all()
            data=BookModelSerializer(book_list_all,many=True).data
            return Response({
                "status": 200,
                "message": "查询成功",
                "results": data
            })
    def post(self,request,*args,**kwargs):
        data=request.data
        serializer=BookModelDeSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        book_obj=serializer.save()
        return Response({
            "status":status.HTTP_200_OK,
            "message": "保存成功",
            "results": BookModelSerializer(book_obj).data

        })

class BookAPIViewV2(APIView):
    def get(self,request,*args,**kwargs):
        book_id=kwargs.get("id")
        if book_id:
            book_bj=Book.objects.get(pk=book_id)
            data=BookModelSerializerV2(book_bj).data
            return Response({
                "status":200,
                "message":"查询成功",
                "results": data
            })

        else:
            book_list_all=Book.objects.all()
            data=BookModelSerializerV2(book_list_all,many=True).data
            return Response({
                "status": 200,
                "message": "查询成功",
                "results": data
            })
    def post(self,request,*args,**kwargs):
        request_data = request.data

        #添加单个
        if isinstance(request_data, dict):
            many = False
            #添加多个
        elif isinstance(request_data, list):
            many = True
        else:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "数据格式有误"
            })

        book_ser = BookModelSerializerV2(data=request_data, many=many)
        book_ser.is_valid(raise_exception=True)
        save = book_ser.save()

        return Response({
            "status": 200,
            "message": '添加图书成功',
            "results": BookModelSerializerV2(save, many=many).data
        })

    def delete(self,request,*args,**kwargs):
        # data=request.data
        # print(data)
        k_id=kwargs.get("id")
        if k_id:
            ids=[k_id]
        else:
            ids=request.data.get("ids")
        de_book=Book.objects.filter(pk__in=ids,is_delete=False).update(is_delete=True)
        if de_book:
            return Response({
                "status":status.HTTP_200_OK,
                "message":"删除成功",
            })
        else:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "删除失败",

             })

    # def put(self, request, *args, **kwargs):  #整体修改
    #
    #     request_data = request.data
    #     book_id = kwargs.get("id")
    #     try:
    #         book_obj = Book.objects.get(pk=book_id)
    #     except:
    #         return Response({
    #             "status": status.HTTP_400_BAD_REQUEST,
    #             "message": "图书不存在",
    #         })
    #
    #     book_ser = BookModelSerializerV2(data=request_data, instance=book_obj)
    #     book_ser.is_valid(raise_exception=True)
    #     save = book_ser.save()
    #
    #     return Response({
    #         "status": 200,
    #         "message": "更新成功",
    #         "results": BookModelSerializerV2(save).data
    #     })
    #
    # def patch(self, request, *args, **kwargs):
    #
    #     request_data = request.data
    #     book_id = kwargs.get("id")
    #     try:
    #         book_obj = Book.objects.get(pk=book_id)
    #     except:
    #         return Response({
    #             "status": status.HTTP_400_BAD_REQUEST,
    #             "message": "图书不存在",
    #         })
    #     book_ser = BookModelSerializerV2(data=request_data, instance=book_obj, partial=True)
    #     book_ser.is_valid(raise_exception=True)
    #     save = book_ser.save()
    #
    #     return Response({
    #         "status": 200,
    #         "message": "局部更新成功",
    #         "results": BookModelSerializerV2(save).data
    #     })


    def patch(self,request,*args,**kwargs):
        re_data=request.data
        book_id=kwargs.get("id")
        if book_id and isinstance(re_data,dict):
            book_ids=[book_id]
            re_data=[re_data]
        elif not book_id and isinstance(re_data,list):
            book_ids=[]
            for dic in re_data:
                d_id=dic.pop("id",None)
                if d_id:
                    book_ids.append(d_id)
                else:
                    return Response({
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": 'id不存在',
                    })
        else:
            return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": '参数有误',
        })

        book_list=[]
        for id in book_ids:
            try:
                book_obj=Book.objects.get(pk=id)
                book_list.append(book_obj)
            except:
                msg=book_ids.index(id)
                re_data.pop(msg)
        book_ser=BookModelSerializerV2(data=re_data,
                                       many=True,
                                       partial=True,
                                       instance=book_list,
                                       context={"request":request}
                                       )
        book_ser.is_valid(raise_exception=True)
        book_ser.save()
        # return Response({
        #     "status":200,
        #     "message":"更新成功"
        # })
        return APIResponse()

