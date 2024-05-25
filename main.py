import os
import requests
from lxml import etree
import json
import base64
from threading import Thread
from queue import Queue
from pprint import pprint
import re


class fq_novel:
    def __init__(self,url,cookie='',number=3):
        self.url = url
        self.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
            'Referer':self.url,
            'cookie':cookie
        }
        self.base = 'https://fanqienovel.com'
        self.title = ''
        self.page = None
        self.name = None
        self.key = self.decrypt()
        self.qurl = Queue()
        self.thread_num = number
        self.get_html()



    def decrypt(self):
        a = 'eyc1ODY3MCc6ICcwJywgJzU4NDEzJzogJzEnLCAnNTg2NzgnOiAnMicsICc1ODM3MSc6ICczJywgJzU4MzUzJzogJzQnLCAnNTg0ODAnOiAnNScsICc1ODM1OSc6ICc2JywgJzU4NDQ5JzogJzcnLCAnNTg1NDAnOiAnOCcsICc1ODY5Mic6ICc5JywgJzU4NzEyJzogJ2EnLCAnNTg1NDInOiAnYicsICc1ODU3NSc6ICdjJywgJzU4NjI2JzogJ2QnLCAnNTg2OTEnOiAnZScsICc1ODU2MSc6ICdmJywgJzU4MzYyJzogJ2cnLCAnNTg2MTknOiAnaCcsICc1ODQzMCc6ICdpJywgJzU4NTMxJzogJ2onLCAnNTg1ODgnOiAnaycsICc1ODQ0MCc6ICdsJywgJzU4NjgxJzogJ20nLCAnNTg2MzEnOiAnbicsICc1ODM3Nic6ICdvJywgJzU4NDI5JzogJ3AnLCAnNTg1NTUnOiAncScsICc1ODQ5OCc6ICdyJywgJzU4NTE4JzogJ3MnLCAnNTg0NTMnOiAndCcsICc1ODM5Nyc6ICd1JywgJzU4MzU2JzogJ3YnLCAnNTg0MzUnOiAndycsICc1ODUxNCc6ICd4JywgJzU4NDgyJzogJ3knLCAnNTg1MjknOiAneicsICc1ODUxNSc6ICdBJywgJzU4Njg4JzogJ0InLCAnNTg3MDknOiAnQycsICc1ODM0NCc6ICdEJywgJzU4NjU2JzogJ0UnLCAnNTgzODEnOiAnRicsICc1ODU3Nic6ICdHJywgJzU4NTE2JzogJ0gnLCAnNTg0NjMnOiAnSScsICc1ODY0OSc6ICdKJywgJzU4NTcxJzogJ0snLCAnNTg1NTgnOiAnTCcsICc1ODQzMyc6ICdNJywgJzU4NTE3JzogJ04nLCAnNTgzODcnOiAnTycsICc1ODY4Nyc6ICdQJywgJzU4NTM3JzogJ1EnLCAnNTg1NDEnOiAnUicsICc1ODQ1OCc6ICdTJywgJzU4MzkwJzogJ1QnLCAnNTg0NjYnOiAnVScsICc1ODM4Nic6ICdWJywgJzU4Njk3JzogJ1cnLCAnNTg1MTknOiAnWCcsICc1ODUxMSc6ICdZJywgJzU4NjM0JzogJ1onLCAnNTg2MTEnOiAn55qEJywgJzU4NTkwJzogJ+S4gCcsICc1ODM5OCc6ICfmmK8nLCAnNTg0MjInOiAn5LqGJywgJzU4NjU3JzogJ+aIkScsICc1ODY2Nic6ICfkuI0nLCAnNTg1NjInOiAn5Lq6JywgJzU4MzQ1JzogJ+WcqCcsICc1ODUxMCc6ICfku5YnLCAnNTg0OTYnOiAn5pyJJywgJzU4NjU0JzogJ+i/mScsICc1ODQ0MSc6ICfkuKonLCAnNTg0OTMnOiAn5LiKJywgJzU4NzE0JzogJ+S7rCcsICc1ODYxOCc6ICfmnaUnLCAnNTg1MjgnOiAn5YiwJywgJzU4NjIwJzogJ+aXticsICc1ODQwMyc6ICflpKcnLCAnNTg0NjEnOiAn5ZywJywgJzU4NDgxJzogJ+S4uicsICc1ODcwMCc6ICflrZAnLCAnNTg3MDgnOiAn5LitJywgJzU4NTAzJzogJ+S9oCcsICc1ODQ0Mic6ICfor7QnLCAnNTg2MzknOiAn55SfJywgJzU4NTA2JzogJ+WbvScsICc1ODY2Myc6ICflubQnLCAnNTg0MzYnOiAn552AJywgJzU4NTYzJzogJ+WwsScsICc1ODM5MSc6ICfpgqMnLCAnNTgzNTcnOiAn5ZKMJywgJzU4MzU0JzogJ+imgScsICc1ODY5NSc6ICflpbknLCAnNTgzNzInOiAn5Ye6JywgJzU4Njk2JzogJ+S5nycsICc1ODU1MSc6ICflvpcnLCAnNTg0NDUnOiAn6YeMJywgJzU4NDA4JzogJ+WQjicsICc1ODU5OSc6ICfoh6onLCAnNTg0MjQnOiAn5LulJywgJzU4Mzk0JzogJ+S8micsICc1ODM0OCc6ICflrrYnLCAnNTg0MjYnOiAn5Y+vJywgJzU4NjczJzogJ+S4iycsICc1ODQxNyc6ICfogIwnLCAnNTg1NTYnOiAn6L+HJywgJzU4NjAzJzogJ+WkqScsICc1ODU2NSc6ICfljrsnLCAnNTg2MDQnOiAn6IO9JywgJzU4NTIyJzogJ+WvuScsICc1ODYzMic6ICflsI8nLCAnNTg2MjInOiAn5aSaJywgJzU4MzUwJzogJ+eEticsICc1ODYwNSc6ICfkuo4nLCAnNTg2MTcnOiAn5b+DJywgJzU4NDAxJzogJ+WtpicsICc1ODYzNyc6ICfkuYgnLCAnNTg2ODQnOiAn5LmLJywgJzU4MzgyJzogJ+mDvScsICc1ODQ2NCc6ICflpb0nLCAnNTg0ODcnOiAn55yLJywgJzU4NjkzJzogJ+i1tycsICc1ODYwOCc6ICflj5EnLCAnNTgzOTInOiAn5b2TJywgJzU4NDc0JzogJ+ayoScsICc1ODYwMSc6ICfmiJAnLCAnNTgzNTUnOiAn5Y+qJywgJzU4NTczJzogJ+WmgicsICc1ODQ5OSc6ICfkuosnLCAnNTg0NjknOiAn5oqKJywgJzU4MzYxJzogJ+i/mCcsICc1ODY5OCc6ICfnlKgnLCAnNTg0ODknOiAn56ysJywgJzU4NzExJzogJ+agtycsICc1ODQ1Nyc6ICfpgZMnLCAnNTg2MzUnOiAn5oOzJywgJzU4NDkyJzogJ+S9nCcsICc1ODY0Nyc6ICfnp40nLCAnNTg2MjMnOiAn5byAJywgJzU4NTIxJzogJ+e+jicsICc1ODYwOSc6ICfmgLsnLCAnNTg1MzAnOiAn5LuOJywgJzU4NjY1JzogJ+aXoCcsICc1ODY1Mic6ICfmg4UnLCAnNTg2NzYnOiAn5bexJywgJzU4NDU2JzogJ+mdoicsICc1ODU4MSc6ICfmnIAnLCAnNTg1MDknOiAn5aWzJywgJzU4NDg4JzogJ+S9hicsICc1ODM2Myc6ICfnjrAnLCAnNTg2ODUnOiAn5YmNJywgJzU4Mzk2JzogJ+S6mycsICc1ODUyMyc6ICfmiYAnLCAnNTg0NzEnOiAn5ZCMJywgJzU4NDg1JzogJ+aXpScsICc1ODYxMyc6ICfmiYsnLCAnNTg1MzMnOiAn5Y+IJywgJzU4NTg5JzogJ+ihjCcsICc1ODUyNyc6ICfmhI8nLCAnNTg1OTMnOiAn5YqoJywgJzU4Njk5JzogJ+aWuScsICc1ODcwNyc6ICfmnJ8nLCAnNTg0MTQnOiAn5a6DJywgJzU4NTk2JzogJ+WktCcsICc1ODU3MCc6ICfnu48nLCAnNTg2NjAnOiAn6ZW/JywgJzU4MzY0JzogJ+WEvycsICc1ODUyNic6ICflm54nLCAnNTg1MDEnOiAn5L2NJywgJzU4NjM4JzogJ+WIhicsICc1ODQwNCc6ICfniLEnLCAnNTg2NzcnOiAn6ICBJywgJzU4NTM1JzogJ+WboCcsICc1ODYyOSc6ICflvognLCAnNTg1NzcnOiAn57uZJywgJzU4NjA2JzogJ+WQjScsICc1ODQ5Nyc6ICfms5UnLCAnNTg2NjInOiAn6Ze0JywgJzU4NDc5JzogJ+aWrycsICc1ODUzMic6ICfnn6UnLCAnNTgzODAnOiAn5LiWJywgJzU4Mzg1JzogJ+S7gCcsICc1ODQwNSc6ICfkuKQnLCAnNTg2NDQnOiAn5qyhJywgJzU4NTc4JzogJ+S9vycsICc1ODUwNSc6ICfouqsnLCAnNTg1NjQnOiAn6ICFJywgJzU4NDEyJzogJ+iiqycsICc1ODY4Nic6ICfpq5gnLCAnNTg2MjQnOiAn5beyJywgJzU4NjY3JzogJ+S6sicsICc1ODYwNyc6ICflhbYnLCAnNTg2MTYnOiAn6L+bJywgJzU4MzY4JzogJ+atpCcsICc1ODQyNyc6ICfor50nLCAnNTg0MjMnOiAn5bi4JywgJzU4NjMzJzogJ+S4jicsICc1ODUyNSc6ICfmtLsnLCAnNTg1NDMnOiAn5q2jJywgJzU4NDE4JzogJ+aEnycsICc1ODU5Nyc6ICfop4EnLCAnNTg2ODMnOiAn5piOJywgJzU4NTA3JzogJ+mXricsICc1ODYyMSc6ICflipsnLCAnNTg3MDMnOiAn55CGJywgJzU4NDM4JzogJ+WwlCcsICc1ODUzNic6ICfngrknLCAnNTgzODQnOiAn5paHJywgJzU4NDg0JzogJ+WHoCcsICc1ODUzOSc6ICflrponLCAnNTg1NTQnOiAn5pysJywgJzU4NDIxJzogJ+WFrCcsICc1ODM0Nyc6ICfnibknLCAnNTg1NjknOiAn5YGaJywgJzU4NzEwJzogJ+WklicsICc1ODU3NCc6ICflraknLCAnNTgzNzUnOiAn55u4JywgJzU4NjQ1JzogJ+ilvycsICc1ODU5Mic6ICfmnpwnLCAnNTg1NzInOiAn6LWwJywgJzU4Mzg4JzogJ+WwhicsICc1ODM3MCc6ICfmnIgnLCAnNTgzOTknOiAn5Y2BJywgJzU4NjUxJzogJ+WunicsICc1ODU0Nic6ICflkJEnLCAnNTg1MDQnOiAn5aOwJywgJzU4NDE5JzogJ+i9picsICc1ODQwNyc6ICflhagnLCAnNTg2NzInOiAn5L+hJywgJzU4Njc1JzogJ+mHjScsICc1ODUzOCc6ICfkuIknLCAnNTg0NjUnOiAn5py6JywgJzU4Mzc0JzogJ+W3pScsICc1ODU3OSc6ICfniaknLCAnNTg0MDInOiAn5rCUJywgJzU4NzAyJzogJ+avjycsICc1ODU1Myc6ICflubYnLCAnNTgzNjAnOiAn5YirJywgJzU4Mzg5JzogJ+ecnycsICc1ODU2MCc6ICfmiZMnLCAnNTg2OTAnOiAn5aSqJywgJzU4NDczJzogJ+aWsCcsICc1ODUxMic6ICfmr5QnLCAnNTg2NTMnOiAn5omNJywgJzU4NzA0JzogJ+S+vycsICc1ODU0NSc6ICflpKsnLCAnNTg2NDEnOiAn5YaNJywgJzU4NDc1JzogJ+S5picsICc1ODU4Myc6ICfpg6gnLCAnNTg0NzInOiAn5rC0JywgJzU4NDc4JzogJ+WDjycsICc1ODY2NCc6ICfnnLwnLCAnNTg1ODYnOiAn562JJywgJzU4NTY4JzogJ+S9kycsICc1ODY3NCc6ICfljbQnLCAnNTg0OTAnOiAn5YqgJywgJzU4NDc2JzogJ+eUtScsICc1ODM0Nic6ICfkuLsnLCAnNTg2MzAnOiAn55WMJywgJzU4NTk1JzogJ+mXqCcsICc1ODUwMic6ICfliKknLCAnNTg3MTMnOiAn5rW3JywgJzU4NTg3JzogJ+WPlycsICc1ODU0OCc6ICflkKwnLCAnNTgzNTEnOiAn6KGoJywgJzU4NTQ3JzogJ+W+tycsICc1ODQ0Myc6ICflsJEnLCAnNTg0NjAnOiAn5YWLJywgJzU4NjM2JzogJ+S7oycsICc1ODU4NSc6ICflkZgnLCAnNTg2MjUnOiAn6K64JywgJzU4Njk0JzogJ+eonCcsICc1ODQyOCc6ICflhYgnLCAnNTg2NDAnOiAn5Y+jJywgJzU4NjI4JzogJ+eUsScsICc1ODYxMic6ICfmrbsnLCAnNTg0NDYnOiAn5a6JJywgJzU4NDY4JzogJ+WGmScsICc1ODQxMCc6ICfmgKcnLCAnNTg1MDgnOiAn6amsJywgJzU4NTk0JzogJ+WFiScsICc1ODQ4Myc6ICfnmb0nLCAnNTg1NDQnOiAn5oiWJywgJzU4NDk1JzogJ+S9jycsICc1ODQ1MCc6ICfpmr4nLCAnNTg2NDMnOiAn5pybJywgJzU4NDg2JzogJ+aVmScsICc1ODQwNic6ICflkb0nLCAnNTg0NDcnOiAn6IqxJywgJzU4NjY5JzogJ+e7kycsICc1ODQxNSc6ICfkuZAnLCAnNTg0NDQnOiAn6ImyJywgJzU4NTQ5JzogJ+abtCcsICc1ODQ5NCc6ICfmi4knLCAnNTg0MDknOiAn5LicJywgJzU4NjU4JzogJ+elnicsICc1ODU1Nyc6ICforrAnLCAnNTg2MDInOiAn5aSEJywgJzU4NTU5JzogJ+iuqScsICc1ODYxMCc6ICfmr40nLCAnNTg1MTMnOiAn54i2JywgJzU4NTAwJzogJ+W6lCcsICc1ODM3OCc6ICfnm7QnLCAnNTg2ODAnOiAn5a2XJywgJzU4MzUyJzogJ+WcuicsICc1ODM4Myc6ICflubMnLCAnNTg0NTQnOiAn5oqlJywgJzU4NjcxJzogJ+WPiycsICc1ODY2OCc6ICflhbMnLCAnNTg0NTInOiAn5pS+JywgJzU4NjI3JzogJ+iHsycsICc1ODQwMCc6ICflvKAnLCAnNTg0NTUnOiAn6K6kJywgJzU4NDE2JzogJ+aOpScsICc1ODU1Mic6ICflkYonLCAnNTg2MTQnOiAn5YWlJywgJzU4NTgyJzogJ+eskScsICc1ODUzNCc6ICflhoUnLCAnNTg3MDEnOiAn6IuxJywgJzU4MzQ5JzogJ+WGmycsICc1ODQ5MSc6ICflgJknLCAnNTg0NjcnOiAn5rCRJywgJzU4MzY1JzogJ+WygScsICc1ODU5OCc6ICflvoAnLCAnNTg0MjUnOiAn5L2VJywgJzU4NDYyJzogJ+W6picsICc1ODQyMCc6ICflsbEnLCAnNTg2NjEnOiAn6KeJJywgJzU4NjE1JzogJ+i3rycsICc1ODY0OCc6ICfluKYnLCAnNTg0NzAnOiAn5LiHJywgJzU4Mzc3JzogJ+eUtycsICc1ODUyMCc6ICfovrknLCAnNTg2NDYnOiAn6aOOJywgJzU4NjAwJzogJ+inoycsICc1ODQzMSc6ICflj6snLCAnNTg3MTUnOiAn5Lu7JywgJzU4NTI0JzogJ+mHkScsICc1ODQzOSc6ICflv6snLCAnNTg1NjYnOiAn5Y6fJywgJzU4NDc3JzogJ+WQgycsICc1ODY0Mic6ICflpognLCAnNTg0MzcnOiAn5Y+YJywgJzU4NDExJzogJ+mAmicsICc1ODQ1MSc6ICfluIgnLCAnNTgzOTUnOiAn56uLJywgJzU4MzY5JzogJ+ixoScsICc1ODcwNic6ICfmlbAnLCAnNTg3MDUnOiAn5ZubJywgJzU4Mzc5JzogJ+WksScsICc1ODU2Nyc6ICfmu6EnLCAnNTgzNzMnOiAn5oiYJywgJzU4NDQ4JzogJ+i/nCcsICc1ODY1OSc6ICfmoLwnLCAnNTg0MzQnOiAn5aOrJywgJzU4Njc5JzogJ+mfsycsICc1ODQzMic6ICfovbsnLCAnNTg2ODknOiAn55uuJywgJzU4NTkxJzogJ+adoScsICc1ODY4Mic6ICflkaInfQ=='
        b = base64.b64decode(a.encode('utf-8')).decode('utf-8').replace("'", '"') #必须是双引号
        c = json.loads(b)
        return c

    def get_html(self):
        respon = requests.get(self.url,headers=self.headers)
        if respon.status_code == 200:
            #print('is ok!')
            self.title = re.search(r'<h1>(?P<name>.*)</h1>',respon.text,re.S).group('name')
            patten = re.findall('<a href="/reader/(?P<page>\d+)" class="chapter-item-title" target="_blank">(?P<title>.*?)</a>',respon.text,re.S)
            patten.pop(0)
            #print(patten)
            for i in patten:
                #print('get_html', i)
                self.qurl.put(i)

        else:
            raise Exception('链接异常')

    def decrypt_content(self,content,title):
        #print(content)
        new_content = []
        for i in content:
            a = ''
            for j in i:
                if str(ord(j)) in self.key.keys():
                    j = self.key[str(ord(j))]
                a += j
            new_content.append(a)
        #print(new_content)
        self.save(new_content,title)


    def save(self,new_content,title):

        if not os.path.exists('小说'):
            os.makedirs('小说')
        if len(new_content) != 0:
            with open(f'.\\小说\\{title}.txt', mode='a', encoding='utf-8') as f:
                for i in new_content:
                    f.write(i + '\n')
            print(f'{title} is ok !')
        else:
            print('请检查你是否为vip用户')




    def get_page(self,args:tuple):
        page_url = self.base + '/reader/' + args[0]
        content = requests.get(page_url,headers=self.headers)
        html = etree.HTML(content.text)
        content = html.xpath('//*[@id="app"]/div/div/div/div[2]/div[2]/div//p/text()')
        #print('输出字符')
        self.decrypt_content(content,args[1])


    def get_info(self):
        while not self.qurl.empty():
            data = self.qurl.get()
            #print('get_info',data)
            self.get_page(data)

    def run(self):
        for _ in range(self.thread_num):
            th = Thread(target=self.get_info)
            th.start()

        print('finished.')


if __name__ == '__main__':
    url = input("请输入番茄小说网址！")
    a = fq_novel(url)
    a.run()


