from django.db import models
from django.conf import settings


class Poem(models.Model):
    title = models.CharField(max_length=200, verbose_name='标题')
    content = models.TextField(verbose_name='正文')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='poems',
        verbose_name='作者'
    )
    image = models.ImageField(upload_to='poems/', blank=True, null=True, verbose_name='配图')
    likes = models.PositiveIntegerField(default=0, verbose_name='点赞数')
    views = models.PositiveIntegerField(default=0, verbose_name='阅读量')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创作时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
        verbose_name = '诗词作品'
        verbose_name_plural = '诗词作品'


class Comment(models.Model):
    poem = models.ForeignKey(
        Poem,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='作品'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='评论者'
    )
    text = models.TextField(verbose_name='评论内容')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')

    def __str__(self):
        return f'{self.author} 评论 {self.poem}'

    class Meta:
        ordering = ['created_at']
        verbose_name = '评论'
        verbose_name_plural = '评论'
