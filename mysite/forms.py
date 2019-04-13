from django import forms
from mysite import models
from captcha.fields import CaptchaField
class PostForm(forms.ModelForm):
    captcha = CaptchaField()
    class Meta:
        model = models.Article
        fields = ['followers', 'following', 'articles']
    
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(self, *args, **kwargs)
        self.fields['followers'].label = 'followers'
        self.fields['following'].label = 'following'
        self.fields['articles'].label = 'articles'
        self.fields['captcha'].label = 'captcha'
        