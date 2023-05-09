import time
import csv
import requests
from io import BytesIO
from PIL import Image
import requests as req
from queue import Queue
from threading import Thread
from bs4 import BeautifulSoup

#使用生产者消费者模式，生产者产生的id链接传给消费者执行
def producer(q,url):  
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    response = requests.get(url=url,headers=headers)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser') 

    ids = soup.select('.dec a')      # 获取包含歌单详情页网址的标签
    q.put(ids)  
    #print(ids)

def consumer(q):
    row = ['id','title','nickname','img','description','count','number of song','number of adding list','share','comment']
    file = open('data.csv', 'w', encoding='utf-8')
    csv_writer = csv.writer(file)  #csv格式写入文件file
    csv_writer.writerow(row)
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }   #设置请求头
    ids = q.get()
    for i in ids:
        url = 'https://music.163.com/' + i['href']  #生产者传递的id链接
        response = requests.get(url=url,headers=headers)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser') 
        
        idd = soup.select('.s-fc7')[0]['href'].split('=')[-1]    
        img = soup.select('img')[0]['data-src']   #图片链接
        res = req.get(img)
        image = Image.open(BytesIO(res.content))  #图片处理
        try:
            image.save(str(time.time())+'.jpg')
        except:
            image.save(str(time.time())+'.png')
            #os.remove(os.getcwd()+f'\\{cnt}.jpg')

        title = soup.select('title')[0].get_text()  #标题
        nickname = soup.select('.s-fc7')[0].get_text()  #昵称
        #print(idd,title,nickname)

        description = soup.select('p')[1].get_text()  #简介
        count = soup.select('strong')[0].get_text()   #播放次数
        song_number = soup.select('span span')[0].get_text()  #歌的数目
        add_lis = soup.select('a i')[1].get_text()   #添加进列表次数
        share = soup.select('a i')[2].get_text()    #分享次数
        comment = soup.select('a i')[4].get_text()  #评论次数
        #print(description,count,song_number,add_lis,share,comment)
        
        csv_writer.writerow([idd,title,nickname,img,description,count,song_number,add_lis,share,comment])
    file.close()

def main():
    start_time = time.time()   #记录时间
    url_list = []
    plist = []
    clist = []

    q = Queue()
    for n in range(0,1300,35):
        url = f'https://music.163.com/discover/playlist/?order=hot&cat=%E8%AF%B4%E5%94%B1&limit=35&offset={n}'
        url_list.append(url)

    for url in url_list:
        p = Thread(target=producer,args=(q,url,))
        plist.append(p)
    for p in plist:  #启动线程
        p.start()
    for p in plist:
        p.join()
    for i in range(40): 
        c = Thread(target=consumer,args=(q,))
        clist.append(c)
    for c in clist:  #启动线程
        c.start()
    for c in clist:
        q.put(None)
    print('time = %f'%(time.time()-start_time))
main()
