from blog_app .models import(
    BlogPost,
    BlogPostCategory,
    BlogPostTag,
)
from rest_framework import serializers
from django.db import models
from django.db.models import fields


# сериализую модель Категорий
class BlogPostCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPostCategory
        fields = '__all__'
        
        
# сериализую модель Тегов 
class BlogPostTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPostTag
        fields = '__all__'
        
        
# простой сериализатор для релизации через функцию со связанными моделями Category & Tag , что бы отображался не только id
class BlogPostFuncSerializer(serializers.ModelSerializer):
    
    # поместил сюда сериализаторы связанных моделей, 
    # что бы видеть не только id, но и содержание
    category = BlogPostCategorySerializer()
    tag = BlogPostTagSerializer(many=True)
       
    class Meta:
        model = BlogPost
        # fields = '__all__'
        
        exclude = ('content', 'created_at', 'status')
        

# простой сериализатор без связанных моделей Category & Tag (иначе дженерики не дают выбирать Category и Tag )
class BlogPostSerializer(serializers.ModelSerializer):   
    class Meta:
        model = BlogPost
        fields = '__all__'
        
        # возможно работать с ограничениями (будет моя последовательность)
        # fields = ('id', 'title', 'img', 'description', 'content', 'category', 'tag')


# сериализатор List для Дженерика List. 
# Выводит все посты, но без подробностей
class BlogPostListSerializer(serializers.ModelSerializer):
    
    # поместил сюда сериализаторы связанных моделей, 
    # что бы видеть не только id, но и содержание
    category = BlogPostCategorySerializer()
    tag = BlogPostTagSerializer(many=True)
    
    class Meta:
        model = BlogPost
        # fields = '__all__'
        
        # # можно конкретно прописать каие поля сериализовать
        # fields = ('id', 'img', 'description')
        
        # или сериализовать все кроме (только у него последовательность своя)
        exclude = ('content', 'created_at', 'status')
        

# сериализатор Detail для Дженерика Detail
# выведет один пост (нужные поля прописал)
class BlogPostDetailSerializer(serializers.ModelSerializer):        
    
    category = BlogPostCategorySerializer()
    tag = BlogPostTagSerializer(many=True)
    
    class Meta:
        model = BlogPost
        # fields = '__all__'
        
        # можно конкретно прописать каие поля сериализовать
        fields = ('title', 'content', 'category', 'tag', 'updated_at')
        
        # # или сериализовать все кроме
        # exclude =('content', 'id', 'created_at', 'status')
