from django.shortcuts import render

# Create your views here.
from django.views.generic.list import ListView
from Blog.models import Article,Category
import markdown2
from django.views.generic import DetailView

class IndexView(ListView):
    """
    首页视图,继承ListView,用于展示文章列表
    """
    template_name = 'home.html'
    context_object_name = "article_list"
    # context_object_name属性用于给上下文变量取名（在模板中使用该名字）

    def get_queryset(self):
        """
        过滤数据,获取所有已经发布的文章,转化为markdown格式
        :return:
        """
        article_list = Article.objects.filter(status='p')
        for article in article_list:
            article.body = markdown2.markdown(article.body, extras=['fenced-code-blocks'],)
            if not article.abstract:
                article.abstract = article.body[:60]
            print(article.abstract)
        return article_list

    def get_context_data(self, **kwargs):
        #添加额外数据,返回文章分类
        kwargs['category_list'] = Category.objects.all().order_by('name')
        return super(IndexView, self).get_context_data(**kwargs)



class ArticleDetailView(DetailView):
    model = Article
    template_name = "detail.html"
    context_object_name = "article"
    pk_url_kwarg = 'article_id'
    def get_object(self, queryset=None):
        obj = super(ArticleDetailView, self).get_object()
        obj.body = markdown2.markdown(obj.body,extras=['fenced-code-blocks'],)
        return obj



class CategoryView(ListView):
# 继承自ListView,用于展示一个列表

    template_name = "index.html"
    # 指定需要渲染的模板

    context_object_name = "article_list"
    # 指定模板中需要使用的上下文对象的名字

    def get_queryset(self):
        #get_queryset 的作用已在第一篇中有介绍，不再赘述
        article_list = Article.objects.filter(category=self.kwargs['cate_id'],status='p')
        # 注意在url里我们捕获了分类的id作为关键字参数（cate_id）传递给了CategoryView，传递的参数在kwargs属性中获取。
        for article in article_list:
            article.body = markdown2.markdown(article.body, )
        return article_list

    # 给视图增加额外的数据
    def get_context_data(self, **kwargs):
        kwargs['category_list'] = Category.objects.all().order_by('name')
        # 增加一个category_list,用于在页面显示所有分类，按照名字排序
        return super(CategoryView, self).get_context_data(**kwargs)

from django.views.decorators.csrf import csrf_protect
from django.core.mail import send_mail
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response,RequestContext

@csrf_protect
def contact(request):
    errors = []
    if request.method == 'POST':
        if not request.POST['subject']:
        # if not request.POST.get('subject', ''):
            errors.append("Subject shouldn't empty.")
        if not request.POST['message']:
        # if not request.POST.get('message', ''):
            errors.append("Message shouldn't empty.")
        if request.POST['email'] and not '@' in request.POST['email']:
            errors.append("Worng email type.")
        if not errors:
            A = request.POST['message'] +  request.POST['email']
            send_mail(
                      request.POST['subject'],
                      A,
                      request.POST.get('keven_susu@126.com'),
                      ['wususua@163.com','kevensusu@gmail.com'],
                fail_silently=False
               )
            print('send')


            return HttpResponseRedirect('/contact/thanks')
    return render_to_response('contact_form.html', {
        'errors': errors,
        'subject': request.POST.get('subject', ''),
        'message': request.POST.get('message', ''),
        'email': request.POST.get('email', ''),
    }, RequestContext(request))

