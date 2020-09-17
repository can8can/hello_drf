from django.urls import path

from app2 import views

urlpatterns=[
    path("book2/",views.BookAPIView.as_view()),
    path("book2/<str:id>/",views.BookAPIView.as_view()),

    path("bgav/",views.BookGenericAPIView.as_view()),
    path("bgav/<str:id>/",views.BookGenericAPIView.as_view()),

    path("bgmv/", views.BookGenericMixinView.as_view()),
    path("bgmv/<str:id>/", views.BookGenericMixinView.as_view()),

    path("bmvs/", views.BookModelViewSet.as_view({"post": "denglu", "get": "count"})),
    path("bmvs/<str:id>/", views.BookModelViewSet.as_view({"post": "denglu", "get": "count"})),

]