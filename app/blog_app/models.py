from django.db import models


# связянная с основной модель Категорий (ForeignKey - у одного поста, одна катгория)
class BlogPostCategory(models.Model):
    title = models.CharField(max_length=25)
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        
    def __str__(self) -> str:
        return self.title
    
    
# связянная с основной модель Тегов (ManyToManyField - каждый пост может иметь несколько тегов. blank=True->допускается отсутствие тегов у поста)
class BlogPostTag(models.Model):
    title = models.CharField(max_length=20)
    
    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        
    def __str__(self) -> str:
        return self.title  
      

# моя основная модель
class BlogPost(models.Model):
    STATUS_CHOISES = (
        ('draft', 'Черновик'),
        ('published', 'Опубликовано')
    )
    title = models.CharField(max_length=20)
    category = models.ForeignKey(BlogPostCategory, on_delete=models.SET_NULL, null=True)
    # img = models.ImageField(upload_to='blog_app/%Y/%m/%d')
    description = models.CharField(max_length=100, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tag = models.ManyToManyField(BlogPostTag, blank=True)
    status = models.CharField(choices=STATUS_CHOISES, default='draft', max_length=15)
    
    # кастомизация админки
    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        
    # кастомизация админки, позволяет видеть title поста, не object...    
    def __str__(self) -> str:
        return self.title
