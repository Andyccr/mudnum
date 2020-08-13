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



You can chose w��wikipedia�� or b���ٶȰٿƣ�
''')
nil = input("�����룺");
#nil = str(input("������ѡ��  :  "))
uid = nil

if uid == 'w':
    def query(content):
        # �����ַ
        cont = quote(content)
        url = 'https://zh.wikipedia.wikimirror.org/wiki/' + cont
        # ����ͷ��
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
        }
        # ���������ַ������ͷ�������������
        req = urllib.request.Request(url=url, headers=headers, method='GET')
        # �������󣬻����Ӧ
        response = urllib.request.urlopen(req)
        # ��ȡ��Ӧ������ı�
        text = response.read().decode('utf-8')
        # ���� _Element ����
        html = etree.HTML(text)
        # ʹ�� xpath ƥ�����ݣ��õ� <div class="mw-parser-output"> �����е��ӽڵ����
        obj_list = html.xpath('//div[@class="mw-parser-output"]/*')
        # �����е��ӽڵ�����л�ȡ���õ� <p> �ڵ����
        for i in range(0, len(obj_list)):
            if 'p' == obj_list[i].tag:
                start = i
                break
        for i in range(start, len(obj_list)):
            if 'p' != obj_list[i].tag:
                end = i
                break
        p_list = obj_list[start:end]
        # ʹ�� xpath ƥ�����ݣ��õ� <p> �����е��ı��ڵ����
        sen_list_list = [obj.xpath('.//text()') for obj in p_list]
        # ���ı��ڵ����ת��Ϊ�ַ����б�
        sen_list = [sen.encode('utf-8').decode() for sen_list in sen_list_list for sen in sen_list]
        # �������ݣ�ȥ���հ�
        sen_list_after_filter = [item.strip('\n') for item in sen_list]
        # ���ַ����б������ַ���������
        return ''.join(sen_list_after_filter)


    if __name__ == '__main__':
       while (True):
        content = input('Word: ')
        result = query(content)

        print("Result: %s" % result)



elif uid == 'b':
    def baike(word):
        def test_url(soup):  # ����Ƿ���¼�ô��������� True or False
            result = soup.find(text=re.compile("�ٶȰٿ�δ��¼�ô���"))
            if result:
                return False
            else:
                return True

        def summary(soup):
            # h1��ǩ���ı����ٿƵ������⣩
            word = soup.h1.text  # �˴�word����ת�� , ��ҪŪ��
            # h2��ǩ���ı����ٿƵĸ����⣩
            if soup.h2:
                word += soup.h2.text

            print(word)

            # ���ٿƵļ�飩
            if soup.find(class_="lemma-summary"):
                print(soup.find(class_="lemma-summary").text)

        def start(word):
            keyword = urllib.parse.urlencode({"word": word})  # �������������URL

            response = urllib.request.urlopen("http://baike.baidu.com/search/word?%s" % keyword)
            html = response.read()
            soup = BeautifulSoup(html, "html.parser")

            if test_url(soup):
                summary(soup)

        try:
            start(word)
        except AttributeError:
            print("�ٶȰٿ�δ��¼�ô���")


    if (__name__ == "__main__"):
        content = str(input("������ؼ���  :  "))
        baike(content)
else:
    print('worry')


