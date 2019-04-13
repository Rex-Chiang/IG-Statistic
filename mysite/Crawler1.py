import os
import re
import requests
import numpy as np
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup as soup
from urllib.request import urlretrieve

import matplotlib
matplotlib.use('Agg')

class Crawler1:
    def __init__(self, url):
        self.url = url
        html = requests.get(self.url) # 對網站發出請求
        page = soup(html.text,'html.parser') # 解析html
        self.script = page.find_all("script")[4].text # 所需資料在第5個script標籤

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

    def ProInfo(self, content):
        like = dict()
        comment = dict()
        # 定義個人照片網址、文章圖片網址、愛心數、留言數的正則表達式
        PROre = re.compile(r"(profile_pic_url_hd\":\")(https:\/\/[\w\W]*)(\",\"requested_by_viewer\")")    
        LIKEre = re.compile(r"(https:\/\/[\w\W]*)(\",\"edge_liked_by\":{\"count\":)(\d*)")
        COMre = re.compile(r"(edge_media_to_comment\":{\"count\":)(\d*)")
        content = content.split("shortcode") # 每篇文章是以屬性shortcode作分段，其中個人照片網址只存在於第一段
        
        for article in content:
            # 取得文章圖片網址、愛心數、留言數
            getlike = LIKEre.search(article)
            getcomment = COMre.search(article)
     
            if getlike != None:
                # 將文章圖片網址、愛心數、留言數紀錄於字典

                like[getlike.group(1)] = int(getlike.group(3).replace(",",""))
                comment[ getlike.group(1)] = int(getcomment.group(2).replace(",",""))
            else:
                # 取得個人照片網址
                pro = PROre.search(article)
                pro = pro.group(2)
        
        return pro, like, comment

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
        pro, like, comment = self.ProInfo(self.script)
        self.Plot(like, comment, account)
        Most_Liked_Posts, Most_Commented_Posts, Least_Liked_Posts, Least_Commented_Posts = self.Statistic(like, comment)
        
        # 將個人照片、最最高愛心數、最高留言數、最低愛心數、最低留言數文章圖片儲存
        self.SaveImage(pro, "pro", account)
        self.SaveImage(Most_Liked_Posts, "mostlike", account)
        self.SaveImage(Most_Commented_Posts, "mostcomment", account)
        self.SaveImage(Least_Liked_Posts, "leastlike", account)
        self.SaveImage(Least_Commented_Posts, "leastcomment", account)
        
        return like[Most_Liked_Posts], comment[Most_Commented_Posts], like[Least_Liked_Posts], comment[Least_Commented_Posts]

if __name__ == '__main__':
    
    ID = input("ID: ")
    url = "https://www.instagram.com/"+ID+"/"
    
    Crawler = Crawler1(url)
    followers, followed, article = Crawler.RE(Crawler.script)
    Most_Liked_Posts, Most_Commented_Posts, Least_Liked_Posts, Least_Commented_Posts = Crawler.Run()
    #Most_Liked_Posts, Most_Commented_Posts, Least_Liked_Posts, Least_Commented_Posts = Crawler.Statistic(like, comment)
