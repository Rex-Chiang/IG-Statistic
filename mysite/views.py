from django.shortcuts import render
from mysite import models
from .Crawler1 import Crawler1
from .Crawler2 import Crawler2
# Create your views here.

def index(request):
    article = models.Article.objects.all()
 
    return render(request, 'index.html', locals())

def posting(request):
    try:
        account = request.POST['account']
    except:
        account = None
        message = '如需查詢，請輸入欲查詢帳號'
    
    if account != None:
        url = "https://www.instagram.com/"+account+"/"
        crawler1 = Crawler1(url)
        crawler2 = Crawler2(url)

        followers, following, article = crawler2.RE(crawler2.page.find_all("script")[4].text)

        account = account.replace(".","_")

        if int(article) <= 12:
            Most_Liked_Posts, Most_Commented_Posts = crawler1.Run(account)
        
        else:
            Most_Liked_Posts, Most_Commented_Posts = crawler2.Run(account)
        
        
        post = models.Article.objects.create(account=account, followers=followers, following=following, articles=article, Most_Liked_Posts=Most_Liked_Posts, Most_Commented_Posts=Most_Commented_Posts)
        post.save()
        message = '查詢成功'
    return render(request, 'posting.html', locals())
