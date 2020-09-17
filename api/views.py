from urllib import response

from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import EmployeeSerializers,EmployeeDeSerializer
from api.models import Employee





class EmployeeAPIView(APIView):
    def get(self,request,*args,**kwargs):
         id=kwargs.get("id")
         if id:
             emp_obj=Employee.objects.get(pk=id)
             # data={
             #     'username':emp_obj.username
             # }
             emp_ser=EmployeeSerializers(emp_obj).data
             print(emp_ser,type(emp_ser))
             return Response({
                 'status':200,
                 'message':'查询成功',
                 'results':emp_ser
             })
         else:
             emp_all=Employee.objects.all()
             emp_ser_all=EmployeeSerializers(emp_all,many=True).data
             #print(emp_ser_all)
             return Response({
                 'status': 200,
                 'message': '查询成功',
                 'results': emp_ser_all
             })


    def post(self,request, *args,**kwargs):
        obj_data=request.data
        # print(obj_data)
        if  not isinstance(obj_data,dict) or obj_data=={}:
            #print("cuowu")
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message":"有错误",

            })
        serializer = EmployeeDeSerializer(data=obj_data)
        if serializer.is_valid():
            a_obj=serializer.save()
            print(a_obj)
            return Response({
                "status":status.HTTP_200_OK,
                "message":"baocun",
                "results":EmployeeSerializers(a_obj).data
        })
        return Response({
            "status":status.HTTP_400_BAD_REQUEST ,
            "message":serializer.errors
        })

