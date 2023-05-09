#1. 导包
import requests
#2. 指定url
url = "https://www.baidu.com"
#3. 使用GET方法发送请求，该方法会返回一个响应对象
response = requests.get(url=url)
#4. 获取响应数据
#print(response.status_code)  # 打印状态码
#print(response.url)          # 打印请求url
print(response.headers)      # 打印响应头头信息
#print(response.text)         #以文本形式打印网页源码
 
#保存数据
response.encoding = 'utf-8'  #指定编码格式，不然打开乱码
text = response.text
with open('./2.html','w',encoding='utf-8') as f:
    f.write(text)