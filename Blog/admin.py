from django.contrib import admin
from Blog.models import Article,Category
# Register your models here.

class Articleadmin(admin.ModelAdmin):
    list_display = ('title', 'create_time', 'last_modifield_time', 'status', 'abstract')


admin.site.register(Article,Articleadmin)
admin.site.register(Category)