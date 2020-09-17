from rest_framework.serializers import ModelSerializer
from rest_framework import exceptions

from rest_framework import serializers
from app1.models import Book, Press
from rest_framework.request import Request


class PressModelSerializer(ModelSerializer):
    class Meta:
        model=Press
        fields=("press_name","address","img")



class BookModelSerializer(ModelSerializer):
    publish=PressModelSerializer()
    class Meta:
        model=Book
        #fields=("book_name","price","pic","haha","press_name","author_name")
        fields = ("book_name", "price","publish")
        #指定不包括的字段
        #exclude = ("is_delete", "status", "id")
        #查询所有字段
        # fields="__all__"
        #查询深度
        # depth=3


class BookModelDeSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = ("book_name", "price", "publish", "authors")
        extra_kwargs = {
            "book_name": {
                "max_length": 8,  # 设置当前字段的最大长度
                "min_length": 2,
                "error_messages": {
                    "max_length": "长度太长了",
                    "min_length": "长度太短了",
                }
            },
            "price": {
                "required": True,
                "decimal_places": 2,
            }
        }
    def validate(self,attrs):
        print(attrs)
        name=attrs.get("book_name")
        book=Book.objects.filter(book_name=name)
        if len(book)>0:
            raise exceptions.ValidationError("图书已经存在")
        return attrs

    def validate_price(self,obj):
        print(obj)
        if obj>100:
            raise exceptions.ValidationError("太贵了")
        return obj



class BookListSerializer(serializers.ListSerializer):
    def update(self, instance, validated_data):
        for index, obj in enumerate(instance):
            self.child.update(obj, validated_data[index])
        return instance


class BookModelSerializerV2(ModelSerializer):
    class Meta:

        list_serializer_class = BookListSerializer

        model=Book
        fields=("book_name", "price", "pic", "publish", "authors")
        extra_kwargs={
            "book_name":{
                "max_length":10,
                "min_length":2,},
            # 只参与反序列化
                "publish": {
                    "write_only": True,  # 指定此字段只参与反序列化
                },
                "authors": {
                    "write_only": True,
                },
                # 只参与序列化
                "pic": {
                    "read_only": True
                }
            }


    def validate(self,attr):
        name=attr.get("book_name")
        book_obj=Book.objects.filter(book_name=name)
        if len(book_obj)>0:
            raise exceptions.ValidationError("图书已经存在")
        return attr

    def validate_price(self,obj):
        re=self.context.get("request")
        print(re.data)
        if obj>100:
            raise exceptions.ValidationError("价格不能高于100")
        return obj







