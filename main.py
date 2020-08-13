import urllib.request
import urllib.parse
import urllib
import requests
from urllib.request import quote
import re
from lxml import etree
from bs4 import BeautifulSoup

print('''

 __       __                  __                                   
/  \     /  |                /  |                                  
$$  \   /$$ | __    __   ____$$ | _______   __    __  _____  ____  
$$$  \ /$$$ |/  |  /  | /    $$ |/       \ /  |  /  |/     \/    \ 
$$$$  /$$$$ |$$ |  $$ |/$$$$$$$ |$$$$$$$  |$$ |  $$ |$$$$$$ $$$$  |
$$ $$ $$/$$ |$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ | $$ | $$ |
$$ |$$$/ $$ |$$ \__$$ |$$ \__$$ |$$ |  $$ |$$ \__$$ |$$ | $$ | $$ |
$$ | $/  $$ |$$    $$/ $$    $$ |$$ |  $$ |$$    $$/ $$ | $$ | $$ |
$$/      $$/  $$$$$$/   $$$$$$$/ $$/   $$/  $$$$$$/  $$/  $$/  $$/ 

www.mudnum.com

.______   ____    ____         ___      .__   __.  _______  ____    ____ 
|   _  \  \   \  /   /        /   \     |  \ |  | |       \ \   \  /   / 
|  |_)  |  \   \/   /        /  ^  \    |   \|  | |  .--.  | \   \/   /  
|   _  <    \_    _/        /  /_\  \   |  . `  | |  |  |  |  \_    _/   
|  |_)  |     |  |         /  _____  \  |  |\   | |  '--'  |    |  |     
|______/      |__|        /__/     \__\ |__| \__| |_______/     |__|     



You can chose w（wikipedia） or b（百度百科）
''')
nil = input("请输入：");
#nil = str(input("请输入选择  :  "))
uid = nil

if uid == 'w':
    def query(content):
        # 请求地址
        cont = quote(content)
        url = 'https://zh.wikipedia.wikimirror.org/wiki/' + cont
        # 请求头部
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
        }
        # 利用请求地址和请求头部构造请求对象
        req = urllib.request.Request(url=url, headers=headers, method='GET')
        # 发送请求，获得响应
        response = urllib.request.urlopen(req)
        # 读取响应，获得文本
        text = response.read().decode('utf-8')
        # 构造 _Element 对象
        html = etree.HTML(text)
        # 使用 xpath 匹配数据，得到 <div class="mw-parser-output"> 下所有的子节点对象
        obj_list = html.xpath('//div[@class="mw-parser-output"]/*')
        # 在所有的子节点对象中获取有用的 <p> 节点对象
        for i in range(0, len(obj_list)):
            if 'p' == obj_list[i].tag:
                start = i
                break
        for i in range(start, len(obj_list)):
            if 'p' != obj_list[i].tag:
                end = i
                break
        p_list = obj_list[start:end]
        # 使用 xpath 匹配数据，得到 <p> 下所有的文本节点对象
        sen_list_list = [obj.xpath('.//text()') for obj in p_list]
        # 将文本节点对象转化为字符串列表
        sen_list = [sen.encode('utf-8').decode() for sen_list in sen_list_list for sen in sen_list]
        # 过滤数据，去掉空白
        sen_list_after_filter = [item.strip('\n') for item in sen_list]
        # 将字符串列表连成字符串并返回
        return ''.join(sen_list_after_filter)


    if __name__ == '__main__':
       while (True):
        content = input('Word: ')
        result = query(content)

        print("Result: %s" % result)



elif uid == 'b':
    def baike(word):
        def test_url(soup):  # 检测是否收录该词条，返回 True or False
            result = soup.find(text=re.compile("百度百科未收录该词条"))
            if result:
                return False
            else:
                return True

        def summary(soup):
            # h1标签的文本（百科的主标题）
            word = soup.h1.text  # 此处word含义转变 , 不要弄混
            # h2标签的文本（百科的副标题）
            if soup.h2:
                word += soup.h2.text

            print(word)

            # （百科的简介）
            if soup.find(class_="lemma-summary"):
                print(soup.find(class_="lemma-summary").text)

        def start(word):
            keyword = urllib.parse.urlencode({"word": word})  # 解析，用于组成URL

            response = urllib.request.urlopen("http://baike.baidu.com/search/word?%s" % keyword)
            html = response.read()
            soup = BeautifulSoup(html, "html.parser")

            if test_url(soup):
                summary(soup)

        try:
            start(word)
        except AttributeError:
            print("百度百科未收录该词条")


    if (__name__ == "__main__"):
        content = str(input("请输入关键词  :  "))
        baike(content)
else:
    print('worry')


