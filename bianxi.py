# coding:utf-8
import os
import urllib
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf-8')



def get_urls():
    """获取所有子链接,及标题,分类"""
    urls = ["http://www.en8848.com.cn/words/bianxi/"]
    for num in range(2, 18):
        url = "http://www.en8848.com.cn/words/bianxi/index_{}.html".format(num)
        urls.append(url)
    fw  = open("urls.txt", 'w')
    for url in urls:
        resp = urllib.urlopen(url)
        html = resp.read()
        soup = BeautifulSoup(html, 'lxml')
        lefts = []
        son_urls = []
        rights = []
        for div in soup.find_all('div'):
            if div.get('class') == ['ch_li_left']:
                title = div.a.get_text()
                lefts.append(title)
                
            if div.get('class') == ['ch_li_right']:
                u = div.h4.a.get('href')
                stitle = div.get_text().split("\r\n")[0].strip()
                son_urls.append("http://www.en8848.com.cn%s"%u)
                rights.append(stitle)
        for i, j, k in zip(lefts, son_urls, rights):
            fw.write("{}@{}@{}\n".format(i, k, j))
        print("url:%s" %(url))
    fw.close()

def get_content():
    """下载内容"""
    num = 0
    for line in open("urls.txt"):
        b, s, u = line.strip().split("@")
        filename = "./词汇辨析/{}.txt".format(s)
        if not os.path.exists(filename):
            try:
                fw = open(filename, 'w')
            except Exception as e:
                """处理文件名不合法,手动修改名称"""
                fw = open("{}.txt".format(num), 'w')
                print num, u
                num += 1
            resp = urllib.urlopen(u)
            html = resp.read()
            soup = BeautifulSoup(html, 'lxml')
            for div in soup.find_all('div'):
                if div.get("class") == ['jxa_content']:
                    for st in div.strings:
                        #print st
                        fw.write(st.strip()+"\n")
            fw.close()
if __name__ == '__main__':
    #get_urls()
    get_content()
