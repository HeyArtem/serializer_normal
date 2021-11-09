from django.urls import path
from blog_app.api.views import(
    blog_post_list,
    blog_post_detail,
    BlogPostListCreateAPIView,
    BlogPostListView,
    BlogPostDetailView,
    BlogPostUpdateView,
    BlogPostUpdateRetrieveView,
    BlogPostDestroyView,
    BlogPostCreateView,
    BlogPostDetailAPIView,
    BlogPostRetrieveView,
)

# активирую разные виды вьюх (представлений)
urlpatterns = [
    
    # ФУНКЦИИ
    # (методы (['GET', 'POST']))
    path('funclist/', blog_post_list),
    
    # (['GET', 'PUT', 'DELETE'])
    path('funcdet/<int:pk>/', blog_post_detail),
    
    # КЛАССЫ
    # через промежуточные классы
    # вывод всех постов, добавленеи нового
    path('class/', BlogPostListCreateAPIView.as_view()),
    
    # через промежуточные классы
    # детельное отображение, обновление и удаление поста
    path('class/detail/<int:pk>/', BlogPostDetailAPIView.as_view()),        
    
    # ДЖЕНЕРИКИ
    # дженерики List
    path('', BlogPostListView.as_view()),
    
    # дженерики Detail
    path('post/<int:pk>/', BlogPostDetailView.as_view()),
    
    # дженерики Update
    path('postup/<int:pk>/', BlogPostUpdateView.as_view()),
    
    # дженерики UpdateRetr
    path('postupre/<int:pk>/', BlogPostUpdateRetrieveView.as_view()),
    
    # дженерик Retrieve!
    path('postre/<int:pk>/', BlogPostRetrieveView.as_view()),
    
    # дженерики Destroy
    path('dest/<int:pk>/', BlogPostDestroyView.as_view()),
    
    # дженерики Create
    path('create/', BlogPostCreateView.as_view()),
]
