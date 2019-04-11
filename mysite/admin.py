from django.contrib import admin
from mysite import models
#from .Crawler1 import Crawler1

# Register your models here.
admin.site.register(models.Article)
admin.site.register(models.PicInfo)
#admin.site.register(Crawler1)
#admin.site.register(Crawler2.Crawler2)
