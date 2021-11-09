from django.shortcuts import render
from rest_framework import serializers
from rest_framework.serializers import Serializer
from blog_app.models import(
    BlogPost,
)
from blog_app.api.serializer import (
    BlogPostFuncSerializer,
    BlogPostSerializer,   
    BlogPostListSerializer,
    BlogPostDetailSerializer,
)
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from rest_framework.generics import get_object_or_404

"""
Реализация сериализатора через функции
    @api_view(['GET', 'POST'])
    def blog_post_list(request):
Выводит список постов и дает возможность Добавить новый

    @api_view(['GET', 'PUT', 'DELETE'])
    def blog_post_detail(request, pk):
Выводит конкретный пост, дает возможность его Обновить, Удалить
"""

# (! Проблем: Посты выводит, но не дает создавать картинка? !)
@api_view(['GET', 'POST'])
def blog_post_list(request):
    
    # метод 'GET' возвращает (показывает) посты
    if request.method =='GET':
        blog_posts = BlogPost.objects.filter(status='published')
        # blog_posts =BlogPost.objects.all()
        serializer = BlogPostFuncSerializer(blog_posts, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # метод 'POST' создает пост (объекты Python в json)
    # для создания использую простой сериализатор
    elif request.method =='POST':
        serializer = BlogPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['GET', 'PUT', 'DELETE'])
def blog_post_detail(request, pk):
    
    # в случае вызова не существуещего поста, работа сервера не завершится, а выведется ошибка 404
    blog_post = get_object_or_404(BlogPost, pk=pk)
    
    if request.method =='GET':
        serializer = BlogPostFuncSerializer(blog_post)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        serializer = BlogPostSerializer(blog_post, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        blog_post.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)    
    

"""
Реализация сериализатора через промежуточную модель 
(Классы) м.у. Функциями и Дженериками
У него нет проверки условия (if method),
а у классов за это отвечают функции (имена: get, post)

Мне нужно дописать:
-Детальный вывод поста
-Обновление конкретного поста
-Удаление
"""

class BlogPostListCreateAPIView(APIView):
    def get(self, request):
        blog_posts = BlogPost.objects.all()
        serializer = BlogPostFuncSerializer(blog_posts, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = BlogPostFuncSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class BlogPostDetailAPIView(APIView):
    def get(self, request, pk):
        blog_post = get_object_or_404(BlogPost, pk=pk)
        serializer = BlogPostDetailSerializer(blog_post)
        
        return Response(serializer.data)
    
    def put(self, request, pk):
        blog_post = get_object_or_404(BlogPost, pk=pk)
        serializer = BlogPostSerializer(blog_post, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        blog_post = get_object_or_404(BlogPost, pk=pk)
        blog_post.delete()
        # serializer = BlogPostSerializer(blog_post, data=request.data)
        
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
# TODO дописать DELETE

"""
Ниже реализация сериализатора через классы с Дженериками
List - выводит список постов, но не весь контент
Detail - детальный (GET ??) вывод одного поста
Update - обновление (PUT) поста, но в форме не выводится тект поста
UpdateRetrieve - обновление поста, в форме присутствует тект поста
Retrieve - детальный вывод поста
Destroy - удаление (DELETE) поста
Create - создание (POST) поста
"""

# List = ListAPIView -> выводит все посты (возможно для главной страницы)), 
# с ограниченной информацией (на главной не нужен content, status и др.). 
# Для него написал отдельный сериализатор (с ограничением по полям)
#   BlogPostListSerializer
class BlogPostListView(generics.ListAPIView):
    queryset = BlogPost.objects.filter(status='published')    
    serializer_class = BlogPostListSerializer    

# Detail = RetrieveAPIView -> выводит один пост с подробностями
# Для него тоже написал отдельный сериализатор (с ограничением по полям)
# ! здесь я использую др.модель сериализатора BlogPostDetailSerializer
class BlogPostDetailView(generics.RetrieveAPIView):
    queryset = BlogPost.objects.filter(status='published')
    serializer_class = BlogPostDetailSerializer

# Update = UpdateAPIView -> возможность обновить пост (но пустая форма)
class BlogPostUpdateView(generics.UpdateAPIView):
    queryset = BlogPost.objects.filter(status='published')
    serializer_class = BlogPostSerializer
    
# TODO разделить view на retriv & update
# UpdateRetrieve = RetrieveUpdateAPIView -> обновление поста (работа с заполненой формой)
# эта модель нужна только что бы посмотреть здесь на нее, на практике их не обьединяют
class BlogPostUpdateRetrieveView(generics.RetrieveUpdateAPIView):
    queryset = BlogPost.objects.filter(status='published')
    serializer_class = BlogPostSerializer 
 
# Retrieve = модель отображает конкретный пост
class BlogPostRetrieveView(generics.RetrieveAPIView):
    queryset = BlogPost.objects.filter(status='published')
    # serializer_class = BlogPostSerializer
    serializer_class = BlogPostDetailSerializer      

# Destroy = DestroyAPIView -> удаляет конкретный пост
class BlogPostDestroyView(generics.DestroyAPIView):
    queryset = BlogPost.objects.filter(status='published')
    serializer_class = BlogPostSerializer
    
# Create = CreateAPIView -> создание поста
class BlogPostCreateView(generics.CreateAPIView):
    queryset = BlogPost.objects.filter(status='published')
    serializer_class = BlogPostSerializer
