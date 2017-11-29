# encoding: utf-8
__author__ = 'ZG'


# 做网页分析的
# pip install bs4

# requests
# 用来做网络请求的
# pip install requests
# pip install lxml

# 1.第一步：把网页数据全部抓下来（requests）
# 2.第部：把抓下来的数据进行过滤，把需要的数据提取出来，把不需要的数据给过滤掉。(bs4)

from bs4 import BeautifulSoup
import requests
import lxml
import time
# pip install echarts-python
from echarts import Echart,Bar,Axis
import json
TEMPERATUR_LIST = []
CITY_LIST =[]
MAX_LIST = []

def get_temperature(url):
    # get/post
    headers = {
        'Host': 'www.weather.com.cn',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/62.0.3202.94 Safari/537.36'
    }
    req = requests.get(url, headers=headers)
    content = req.content

    soup = BeautifulSoup(content, 'lxml')
    conMidtab = soup.find('div', class_='conMidtab')
    conMidtab2_list = conMidtab.find_all('div', class_='conMidtab2')
    for x in conMidtab2_list:
        tr_list = x.find_all('tr')[2:]
        province = ''
        for index, tr in enumerate(tr_list):
            #  如果是第0个tr个标签 ，那么城市名和省份名是放在一起的
            if index == 0:
                td_list = tr.find_all('td')
                province = td_list[0].text.replace('\n', '')
                city = td_list[1].text.replace('\n', '')
                max = td_list[4].text.replace('\n', '')
            else:
                td_list = tr.find_all('td')
                city = td_list[0].text.replace('\n', '')
                max = td_list[3].text.replace('\n', '')
            TEMPERATUR_LIST.append({
                'city': province+city,
                'max': max
            })

            CITY_LIST.append(province+city)
            MAX_LIST.append(max)

def main():
    # urls=['http://www.weather.com.cn/textFC/hb.shtml',
    #       'http://www.weather.com.cn/textFC/db.shtml',
    #       'http://www.weather.com.cn/textFC/hd.shtml',
    #       'http://www.weather.com.cn/textFC/hz.shtml',
    #       'http://www.weather.com.cn/textFC/hn.shtml',
    #       'http://www.weather.com.cn/textFC/xb.shtml',
    #       'http://www.weather.com.cn/textFC/xn.shtml',
    #       ]
    # for url in urls:
    #     get_temperature(url)
    #     time.sleep(2)
    #
    # line =  json.dumps(TEMPERATUR_LIST, ensure_ascii=False)
    # with open('temperature.json','w') as fp:
    #     fp.write(line.encode('utf-8'))

    with open('temperature.json','r') as fp:
        TEMPERATUR_LIST = json.load(fp, encoding='utf-8')

    SORTED_TEMPERATURE_LIST = sorted(TEMPERATUR_LIST, lambda x,y:cmp(int(y['max']),int(x['max'])))
    TOP20_TEMPERATURE_LIST  = SORTED_TEMPERATURE_LIST[0:20]
    TOP20_CITY_LIST = []
    TOP20_MAX_LIST = []
    for city_max in TOP20_TEMPERATURE_LIST:
        TOP20_CITY_LIST.append(city_max['city'])
        TOP20_MAX_LIST.append(city_max['max'])

    echart = Echart(u'全国最高温度排名',u'ZG爬虫')
    bar= Bar(u'最高温度', TOP20_MAX_LIST)
    axis = Axis('category', 'bottom', data= TOP20_CITY_LIST)
    echart.use(bar)
    echart.use(axis)
    echart.plot()

if __name__ == '__main__':
    main()
# 所有的城市都是放在属于某个省或者直辖市的表格中的
# 真正有用的数据是从第32个tr开始的（下标是从0开始）
# 真正有用的第0个tr中的第0个td，表示的是当前这个表格的省份或者直辖市的名字
# 其余有用的tr的第0个td,实际上就是表示了当前这个城市的
