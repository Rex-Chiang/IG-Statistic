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

import matplotlib
matplotlib.use('Agg')

class Crawler2:
    def __init__(self, url):
        self.url = url
        html = requests.get(self.url) # 對網站發出請求
        self.page = soup(html.text,'html.parser') # 解析html
        
    def RE(self, content):
        # 定義被追蹤數、追蹤數、發文數的正則表達式
        FOLLOWre = re.compile(r"(edge_followed_by\":{\"count\":)(\d*)")
        FOLLOWEDre = re.compile(r"(edge_follow\":{\"count\":)(\d*)")
        ARTICLEre = re.compile(r"(edge_owner_to_timeline_media\":{\"count\":)(\d*)")
        # 取得追蹤數、追蹤數、發文數
        followers = FOLLOWre.search(content).group(2)
        followed = FOLLOWEDre.search(content).group(2)
        article = ARTICLEre.search(content).group(2)
        
        return followers, followed, article
    
    def ProInfo(self, page):
        script = page.find_all("script")[8].text # 所需資料在第9個script標籤
        PROre = re.compile(r"(profile_pic_url_hd\":\")(https:\/\/[\w\W]*)(\",\"requested_by_viewer\")") # 定義個人照片網址的正則表達式
        getpro = PROre.search(script).group(2) # 取得個人照片網址
        
        return getpro
    
    def PicInfoBEF(self, page, i):
        # 前12篇的文章內容
        script = page.find_all("script")[8].text # 所需資料在第9個script標籤
        script = script.split("shortcode")[i+1] # 每篇文章是以屬性shortcode作分段
        # 定義文章圖片網址、愛心數、留言數的正則表達式
        PICre = re.compile(r"(\":\")(https:\/\/[\w\W]*)(\",\"edge_liked_by\")")    
        LIKEre = re.compile(r"(\"edge_liked_by\":{\"count\":)(\d*)")
        COMre = re.compile(r"(\"edge_media_to_comment\":{\"count\":)(\d*)")
        # 取得文章圖片網址、愛心數、留言數
        getpic = PICre.search(script).group(2)
        getlike = LIKEre.search(script).group(2).replace(",","")
        getcomment = COMre.search(script).group(2).replace(",","")
    
        return getpic, int(getlike), int(getcomment)
    
    def PicInfoAFT(self, page, i):
        # 12篇後的文章內容
        # 取得文章圖片網址、愛心數
        getpic = page.find_all('div',{'class':'KL4Bh'})[i].find('img',{'class':'FFVAD'})["src"]
        if page.find('div',{'class':'Nm9Fw'}):
            getlike = page.find('div',{'class':'Nm9Fw'}).find('span').text.replace(",","")
        else:
            getlike = 45
        # 取得留言數，留言數小於等於4者html本身不顯示因此設定為0
        if page.find('li',{'class':'lnrre'}):
            getcomment = page.find('li',{'class':'lnrre'}).find('span').text.replace(",","")
        else:
            getcomment = 0
            
        return getpic, int(getlike), int(getcomment)
    
    def Plot(self, like, comment, account):
        # 分別繪出愛心數、留言數的曲線並儲存
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
    
    def Statistic(self, like, comment):
        # 原本的like、comment字典形式為[圖片網址:愛心數]、[圖片網址:留言數]
        # 為了以愛心數、留言數做鍵查詢將字典形式改為[愛心數:圖片網址]、[留言數:圖片網址]
        TransLike = {v : k for k, v in like.items()}
        TransComm = {v : k for k, v in comment.items()}
        # 取得最高愛心數、最高留言數、最低愛心數、最低留言數文章
        Most_Liked_Posts = TransLike[max(like.values())]
        Most_Commented_Posts = TransComm[max(comment.values())]
        Least_Liked_Posts = TransLike[min(like.values())]
        Least_Commented_Posts = TransComm[min(comment.values())]
        
        return Most_Liked_Posts, Most_Commented_Posts, Least_Liked_Posts, Least_Commented_Posts
    
    def SaveImage(self, img, path, account):
        img_path = os.path.join("/home/rex/桌面/IG-project/IGstatistic/mysite/static/"+path+"/"+account)
        urlretrieve(img, img_path)
    
    def Run(self, account="ID"):
        like = dict()
        comment = dict()
        
        chrome_options = webdriver.ChromeOptions() # 對Chrome瀏覽器設定
        chrome_options.add_argument('--headless') # 啟動無頭模式，不顯示瀏覽畫面
        chrome_options.add_argument('user-agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36"') # 設定user agent
        driver = webdriver.Chrome(executable_path='/usr/local/share/chromedriver', chrome_options=chrome_options)
        driver.get(self.url) # 對網站發出請求
        time.sleep(1)
        driver.find_element_by_xpath("//div/a/div[@class='eLAPa']").click() # 點擊第一篇文章
        time.sleep(1)
        
        for i in range(0, 34):
            try:
                NextPage = soup(driver.page_source,'html.parser') # 解析html
                # 取得前12篇的文章內容
                if i < 12:
                    getpic, getlike, getcomment = self.PicInfoBEF(NextPage, i)
                    like[getpic] = getlike
                    comment[getpic] = getcomment
                # 取得12篇後的文章內容
                else:
                    getpic, getlike, getcomment = self.PicInfoAFT(NextPage, i) 
                    like[getpic] = getlike
                    comment[getpic] = getcomment
                    
                driver.find_element_by_xpath("//div/a[@class='HBoOv coreSpriteRightPaginationArrow']").click() # 點擊下一篇文章
                time.sleep(1)
            except:
                print("ERROR")
        
        driver.quit()
        Most_Liked_Posts, Most_Commented_Posts, Least_Liked_Posts, Least_Commented_Posts = self.Statistic(like, comment)
        self.Plot(like, comment, account)
        
        pro = self.ProInfo(NextPage)
        # 將個人照片、最最高愛心數、最高留言數、最低愛心數、最低留言數文章圖片儲存
        self.SaveImage(pro, "pro", account)
        self.SaveImage(Most_Liked_Posts, "mostlike", account)
        self.SaveImage(Most_Commented_Posts, "mostcomment", account)
        self.SaveImage(Least_Liked_Posts, "leastlike", account)
        self.SaveImage(Least_Commented_Posts, "leastcomment", account)
        
        return like[Most_Liked_Posts], comment[Most_Commented_Posts], like[Least_Liked_Posts], comment[Least_Commented_Posts]
    
if __name__ == "__main__":
    
    ID = input("ID: ")
    url = "https://www.instagram.com/"+ID+"/"
    Crawler1 = Crawler1.Crawler1(url)
    Crawler2 = Crawler2(url)
    
    followers, followed, article = Crawler2.RE(Crawler2.page.find_all("script")[4].text)

    if int(article) <= 12:
        Most_Liked_Posts, Most_Commented_Posts, Least_Liked_Posts, Least_Commented_Posts = Crawler1.Run()        
        
    else:
        Most_Liked_Posts, Most_Commented_Posts, Least_Liked_Posts, Least_Commented_Posts = Crawler2.Run()
        

