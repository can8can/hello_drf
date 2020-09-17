from rest_framework.serializers import ModelSerializer
from rest_framework import exceptions

from rest_framework import serializers
from app1.models import Book, Press
from rest_framework.request import Request

from app1.serializers import BookListSerializer


class BookModelSerializer(ModelSerializer):
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







