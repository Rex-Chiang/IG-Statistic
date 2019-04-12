import requests
import os
import re
import time
import numpy as np
import matplotlib.pyplot as plt
from .Crawler1 import Crawler1
from selenium import webdriver
from bs4 import BeautifulSoup as soup
from urllib.request import urlretrieve

class Crawler2:
    def __init__(self, url):
        self.url = url
        html = requests.get(self.url)
        self.page = soup(html.text,'html.parser')        
        
    def RE(self, content):
        
            FOLLOWre = re.compile(r"(edge_followed_by\":{\"count\":)(\d*)")
            FOLLOWEDre = re.compile(r"(edge_follow\":{\"count\":)(\d*)")
            ARTICLEre = re.compile(r"(edge_owner_to_timeline_media\":{\"count\":)(\d*)")
            
            followers = FOLLOWre.search(content).group(2)
            followed = FOLLOWEDre.search(content).group(2)
            article = ARTICLEre.search(content).group(2)
            
            return followers, followed, article
    
    def ProInfo(self, page):
        script = page.find_all("script")[8].text
        PROre = re.compile(r"(profile_pic_url_hd\":\")(https:\/\/[\w\W]*)(\",\"requested_by_viewer\")")
        getpro = PROre.search(script).group(2)
        
        return getpro
    
    def PicInfoBEF(self, page, i):
        
        script = page.find_all("script")[8].text
        script = script.split("shortcode")[i+1]
        
        PICre = re.compile(r"(\":\")(https:\/\/[\w\W]*)(\",\"edge_liked_by\")")    
        LIKEre = re.compile(r"(\"edge_liked_by\":{\"count\":)(\d*)")
        COMre = re.compile(r"(\"edge_media_to_comment\":{\"count\":)(\d*)")
        
        getpic = PICre.search(script).group(2)
        getlike = LIKEre.search(script).group(2)
        getcomment = COMre.search(script).group(2)
    
        return getpic, int(getlike), int(getcomment)
    
    def PicInfoAFT(self, page, i):
        
        getpic = page.find_all('div',{'class':'KL4Bh'})[i].find('img',{'class':'FFVAD'})["src"]
        getlike = page.find('div',{'class':'Nm9Fw'}).find('span').text
        
        if page.find('li',{'class':'lnrre'}):
            getcomment = page.find('li',{'class':'lnrre'}).find('span').text
        else:
            getcomment = 0
            
        return getpic, int(getlike), int(getcomment)
    
    def Statistic(self, like, comment):
        TransLike = {v : k for k, v in like.items()}
        TransComm = {v : k for k, v in comment.items()}
    
        Most_Liked_Posts = TransLike[max(like.values())]
        Most_Commented_Posts = TransComm[max(comment.values())]
        Least_Liked_Posts = TransLike[min(like.values())]
        Least_Commented_Posts = TransComm[min(comment.values())]
        
        return Most_Liked_Posts, Most_Commented_Posts, Least_Liked_Posts, Least_Commented_Posts
    
    def Plot(self, like, comment, account):
        #LIKES, COMMS = zip(*info.keys())
        x = np.arange(1, len(like.values())+1, 1)
        plt.plot(x, like.values(), "bo-", lw = 1, ms = 5, alpha=0.7, mfc='orange', label= "LIKES")
        plt.grid(color='g',linestyle='--', linewidth=1,alpha=0.4)
        plt.xlabel("ARTICLES")
        plt.ylabel("COUNTS")
        plt.xlim((1, len(like.values())))
        plt.legend()
        plt.savefig("/home/rex/桌面/IG-project/IGstatistic/mysite/static/likes/"+account)
        plt.close()
        #plt.show()
        plt.plot(x, comment.values(), "ro-", lw = 1, ms = 5, alpha=0.7, mfc='orange', label= "COMMENTS")
        plt.grid(color='g',linestyle='--', linewidth=1,alpha=0.4)
        plt.xlabel("ARTICLES")
        plt.ylabel("COUNTS")
        plt.xlim((1, len(like.values())))
        plt.legend()
        plt.savefig("/home/rex/桌面/IG-project/IGstatistic/mysite/static/comments/"+account)
        plt.close()
        #plt.show()
    
    def Run(self, account="ID"):
        like = dict()
        comment = dict()
        
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless') # 啟動無頭模式  
        chrome_options.add_argument('user-agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36"')
        driver = webdriver.Chrome(executable_path='/usr/local/share/chromedriver', chrome_options=chrome_options)
        driver.get(self.url)
        time.sleep(1)
        driver.find_element_by_xpath("//div/a/div[@class='eLAPa']").click()
        time.sleep(1)
        
        for i in range(0, 34):      
            NextPage = soup(driver.page_source,'html.parser')        
            pro = self.ProInfo(NextPage)
            
            if i < 12:
                getpic, getlike, getcomment = self.PicInfoBEF(NextPage, i)
                like[getpic] = getlike
                comment[getpic] = getcomment
            else:
                getpic, getlike, getcomment = self.PicInfoAFT(NextPage, i) 
                like[getpic] = getlike
                comment[getpic] = getcomment
                
            driver.find_element_by_xpath("//div/a[@class='HBoOv coreSpriteRightPaginationArrow']").click()
            time.sleep(1)
        
        driver.quit()
        Most_Liked_Posts, Most_Commented_Posts, Least_Liked_Posts, Least_Commented_Posts = self.Statistic(like, comment)
        self.Plot(like, comment, account)
        img_path = os.path.join("/home/rex/桌面/IG-project/IGstatistic/mysite/static/pro/"+account)
        urlretrieve(pro, img_path)
        
        return like[Most_Liked_Posts], comment[Most_Commented_Posts]
    
if __name__ == "__main__":
    
    ID = input("ID: ")
    url = "https://www.instagram.com/"+ID+"/"
    Crawler1 = Crawler1.Crawler1(url)
    Crawler2 = Crawler2(url)
    
    followers, followed, article = Crawler2.RE(Crawler2.page.find_all("script")[4].text)

    if int(article) <= 12:
        pro, like, comment = Crawler1.Run()        
        
    else:
        pro, like, comment = Crawler2.Run()
        

