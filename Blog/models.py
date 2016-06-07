from django.db import models

class Article(models.Model):
    STATUS_CHOICES = (
        ('d', 'Draft'),
        ('p', 'Published'),
    )
    #在 status 时说明
    title = models.CharField('标题', max_length=80)
    body = models.TextField('正文')                                                 # TextField      储存大文本字符
    create_time = models.DateTimeField('创建时间', auto_now_add=True)               # auto_now_add  文章创建时自动创建时间
    last_modifield_time = models.DateTimeField('修改时间', auto_now=True)           # auto_now       修改文章时自动修改时间
    status = models.CharField('文章状态', max_length=1, choices=STATUS_CHOICES)
    abstract = models.CharField('摘要', max_length=60, blank=True, null=True, help_text="可选,如若为空将摘取正文的前60个字符")
    views = models.PositiveIntegerField('浏览量', default=0)                        # 阅览量，PositiveIntegerField存储非负整数
    likes = models.PositiveIntegerField('点赞数', default=0)
    topped = models.BooleanField('置顶', default=False)                             # 是否顶置, BooleanField  储存布尔值(True 或者 False)
    category = models.ForeignKey('Category', verbose_name='分类', null=True, on_delete=models.SET_NULL)              #文章的分类, 数据库中的外键

    def __str__(self):
        # 交互显示器表示字符串
        return self.title

    class Meta:
        ordering = ['-last_modifield_time']



class Category(models.Model):
    """
    储存文章分类信息的表
    """
    name = models.CharField('类名', max_length=20)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_modified_time = models.DateTimeField('修改时间', auto_now=True)

    def __str__(self):
        return self.name
