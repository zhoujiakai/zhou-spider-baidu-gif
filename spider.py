"""
 爬虫常用库:
    发送请求 requests
    处理html BeautifulSoup
    解释器 lxml
"""
import json
import os
import requests

# 搜索关键词
query_word = "搞笑猫狗gif"

# 一共需要下载多少张gif
totalnum = 270
filename = 1

# 请求头部
header = {"Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2", "Connection": "keep-alive",
          "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0",
          "Upgrade-Insecure-Requests": "1"}


# 主函数
def spider_baidu_gif():
    # 创建保存图片的文件夹
    if not os.path.exists('images'):
        os.mkdir('images')
    # 下载页码
    pagenum = 30
    while pagenum < totalnum+30:
        # 请求链接
        url = "https://image.baidu.com/search/acjson?tn=resultjson_com&logid=9388361316650668372&ipn=rj&ct=201326592" \
              "&is=&fp=result&fr=&word=" + query_word + \
              "&queryWord=" + query_word + \
              "&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&hd=&latest=&copyright=&s=&se=&tab=&width=&height" \
              "=&face=0&istype=2&qc=&nc=1&expermode=&nojc=&isAsync=&pn=" + str(pagenum) + \
              "&rn=30&gsm=5a&1658995244722= "
        # 获取所有图片链接
        gif_urls = get_img_urls(url)
        # 开始下载图片
        for gif_url in gif_urls:
            download_img(gif_url)
        pagenum += 30
    print('下载完毕')


# 爬取链接
def get_img_urls(url):
    response = requests.get(url=url, headers=header)
    # 取出返回的json内容
    content = response.content
    # 将bytes转换成str
    content = content.decode('utf-8', errors='ignore')
    # 将str转换成json
    content = json.loads(content)
    # 取出gif列表
    data = content['data']
    gif_urls = []
    # 取出所有gif链接保存到 gif_urls
    for obj in data:
        try:
            gif_url = obj['replaceUrl'][0]['ObjURL']
            gif_urls.append(gif_url)
        except:
            pass
    return gif_urls


# 下载图片
def download_img(gif_url):
    # 图片名
    global filename
    # 输出提示文字
    print('正在下载: ', gif_url)
    # 创建文件
    with open(f'images/{filename}.gif', 'wb') as f:
        # 写入图片
        f.write(requests.get(url=gif_url).content)
    print('已下载gif: ', str(filename) + '.gif')
    filename += 1


# 运行主函数
spider_baidu_gif()
