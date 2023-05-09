import requests
from lxml import etree

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
#name_path11='//*[@id="content"]/div/div[1]/ol/li[1]/div/div[2]/div[1]/a/span[1]'
#name_path12='//*[@id="content"]/div/div[1]/ol/li[2]/div/div[2]/div[1]/a/span[1]'
#name_path21='//*[@id="content"]/div/div[1]/ol/li[1]/div/div[2]/div[1]/a/span[1]'
name_path_lis=['//*[@id="content"]/div/div[1]/ol/li['+str(i+1)+']/div/div[2]/div[1]/a/span[1]' for i in range(25)]
#url1='https://movie.douban.com/top250'
#url2='https://movie.douban.com/top250?start=25&filter='
url_lis=['https://movie.douban.com/top250?start='+str(i*25)+'&filter=' for i in range(10)]
names=[]
f=open('D:/Project/Python/week12Crawler/top250.txt','w',encoding='utf8')
for i,url in enumerate(url_lis):
    web_data=requests.get(url,headers=headers)
    web_html=etree.HTML(web_data.text)
    for j,name_path in enumerate(name_path_lis):
        name=web_html.xpath(name_path)
        f.write('no.'+str(i*j)+' '+name[0].text+'\n')
        print(name[0].text)
f.close()