from django.shortcuts import render
from mysite import models
from .Crawler1 import Crawler1
# Create your views here.

def index(request):
    article = models.Article.objects.all()
    Crawler = Crawler1("https://www.instagram.com/rickys_cookingdiary/")
    pro, like, comment = Crawler.Run()
    return render(request, 'index.html', locals())

def posting(request):
    try:
        account = request.POST['account']
    except:
        account = None
        message = '如需查詢，請輸入欲查詢帳號'
    
    if account != None:
        post = models.Article.objects.create(account=account, pro="https", followers=0, followered=0, articles=0)
        post.save()
        message = '查詢成功'
    return render(request, 'posting.html', locals())
