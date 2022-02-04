import datetime
import json
import re
import pandas as pd
import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
}
con = create_engine("mysql+mysqlconnector://root:147123@localhost:3306/ksh")
# 历史数据
def lishishuju():
    df = pd.read_csv('demo/csv/丁香园国内疫情.csv', engine='c') # 读取数据

    df = df.sort_values('累计确诊', ascending=False) # 根据累计确诊去排序-降序

    df = df.drop_duplicates('省份', keep='first') # 根据省份去重,取第一次出现的数据

    df['省份'] = df['省份'].str.strip('省').str.strip('市').str.strip('壮族自治区').str.strip('自治区').str.strip('回族自治区').str.strip('维吾尔自治区')

    url = 'https://api.inews.qq.com/newsqa/v1/query/pubished/daily/list?province=湖北'
    data = json.loads(requests.get(url, headers=headers).content.decode())['data']

    for i in df['省份']:
        if i != '湖北':
            url = 'https://api.inews.qq.com/newsqa/v1/query/pubished/daily/list?province=' + i
            x = json.loads(requests.get(url).content.decode())['data']
            data = data + x

    def funx(x):
        if len(x) == 3:
            x = x + '0'
        return x

    df = pd.DataFrame(data)
    x = df['year'].astype('str') + '.'
    y = (df['date'].astype('str'))
    y = y.apply(lambda x: funx(x))

    df['dateId'] = x + y
    df['dateId'] = pd.DatetimeIndex(df['dateId']).astype('str').str[:7]

    df.to_csv('demo/csv/国内疫情数据.csv', index=False, encoding='utf-8-sig')
    df.to_sql('gnlssj', if_exists='replace', con=con, index=False)
    con.execute('ALTER TABLE gnlssj ADD id INT(16) NOT NULL PRIMARY KEY AUTO_INCREMENT FIRST;')  # 添加自增字段id

# 中国今日疫情情况
def yqday():
    url = 'https://api.inews.qq.com/newsqa/v1/query/inner/publish/modules/list?modules=statisGradeCityDetail,diseaseh5Shelf'
    data = json.loads(requests.post(url=url, headers=headers).content.decode())['data']
    x = data['statisGradeCityDetail']
    y = []
    for i in x:
        j = [i['province'] + i['city'], i['confirmAdd'], i['nowConfirm'], i['grade']]
        y.append(j)

    x = ['address', 'addqz', 'xyqz', 'fxqy']

    # 使用create_engine + pandas 快捷保存数据库
    df = pd.DataFrame(y, columns=x)
    df.to_sql('bentuxianyou31', if_exists='replace', con=con, index=False)
    con.execute('ALTER TABLE bentuxianyou31 ADD id INT(16) NOT NULL PRIMARY KEY AUTO_INCREMENT FIRST;') # 添加自增字段id
    with open('demo/data/中国疫情.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False, indent=4))

    pd.DataFrame(y).to_csv('demo/csv/近31省市区现有本土病例.csv', index=False, encoding='utf-8', header=x)
    # 使用create_engine + pandas 快捷保存数据库


# 中国每日疫情
def yqveryday():
    url = 'https://file1.dxycdn.com/2021/1228/171/2851867762198723253-135.json?t=27344362'  # url
    head_data = requests.get(url=url, headers=headers).content  # 获取数据
    data = json.loads(head_data)['data'] # 把取到的数据返回
    # 使用pandas快捷保存csv
    pd.DataFrame(data).to_csv('demo/csv/丁香园国内每日疫情情况.csv', encoding='utf-8', index=False)
    pd.DataFrame(data).to_sql('mrsj', if_exists='replace', con=con, index=False)
    con.execute('ALTER TABLE mrsj ADD id INT(16) NOT NULL PRIMARY KEY AUTO_INCREMENT FIRST;') # 添加自增字段id

# 实时热点
def ssrd():
    url = 'https://opendata.baidu.com/data/inner?tn=reserved_all_res_tn&dspName=iphone&from_sf=1&dsp=iphone&resource_id=28565&alr=1&query=%E5%9B%BD%E5%86%85%E6%96%B0%E5%9E%8B%E8%82%BA%E7%82%8E%E6%9C%80%E6%96%B0%E5%8A%A8%E6%80%81&cb=jsonp_1642854207390_27502'
    data = json.loads(requests.get(url=url, headers=headers).content.decode().split('(')[1][:-1])['Result'][0]['DisplayData']['result'][
        'items']
    with open('demo/data/实时热点.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False, indent=4))
    pd.DataFrame(data).to_sql('ssrd', if_exists='replace', con=con, index=False)
    con.execute('ALTER TABLE ssrd ADD id INT(16) NOT NULL PRIMARY KEY AUTO_INCREMENT FIRST;') # 添加自增字段id

# 国内各省目前疫情
def parse():
    data = []  # 定义全局列表t
    data1 = []
    url = 'https://ncov.dxy.cn/ncovh5/view/pneumonia'  # url

    head_data = requests.get(url=url, headers=headers).content # 获取数据
    res = BeautifulSoup(head_data, 'html.parser') # 利用bs4解析数据
    res = res.find('script', {'id': 'getAreaStat'}).text  # 利用bs4获取国内的数据
    res = re.findall('try \{ window.getAreaStat = (.*)}catch', res, re.S)[0] # 利用正则表达式先取得里面的所有数据
    res = re.findall('\{(.*?)]}', res) # 利用正则表达式再去取每个省的数据
    for i in res:
        provinceName = re.findall('"provinceName":"(.*?)"', i) # 取省份名
        cityName = re.findall('"cityName":"(.*?)"', i) # 取城市名
        if len(cityName) == 0:                      # 判断城市的长度是否为0
            cityName = provinceName               # 为零则把城市 = 省份 方便后面的保存
        else:
            cityName.insert(0, provinceName[0])          # 在城市列表最开始的位置插入省份名
        currentConfirmedCount = re.findall('"currentConfirmedCount":(.*?),', i) # 取现有确诊
        confirmedCount = re.findall('"confirmedCount":(.*?),', i) # 去取累计确诊
        curedCount = re.findall('"curedCount":(.*?),', i) # 取累计治愈
        deadCount = re.findall('"deadCount":(.*?),', i) # 取累计死亡

        for i in range(0, len(currentConfirmedCount)):   # 遍历存到列表t
            data.append({
                'provinceName': cityName[0],
                'cityName': cityName[i],
                'currentConfirmedCount': currentConfirmedCount[i],
                'confirmedCount': confirmedCount[i],
                'curedCount': curedCount[i],
                'deadCount': deadCount[i],
            })
        for i in range(0, len(currentConfirmedCount)):   # 遍历存到列表t
            data1.append({
                '省份': cityName[0],
                '城市': cityName[i],
                '现有确诊': currentConfirmedCount[i],
                '累计确诊': confirmedCount[i],
                '累计治愈': curedCount[i],
                '累计死亡': deadCount[i],
            })
    pd.DataFrame(data1).to_csv('demo/csv/丁香园国内疫情.csv', encoding='utf-8', index=False)
    pd.DataFrame(data).to_sql('xyyq', if_exists='replace', con=con, index=False)
    con.execute('ALTER TABLE xyyq ADD id INT(16) NOT NULL PRIMARY KEY AUTO_INCREMENT FIRST;') # 添加自增字段id

# 风险地区
def fxdq():
    url = 'https://file1.dxycdn.com/2021/0202/196/1680100273140422643-135.json'
    resdata = json.loads(requests.get(url, headers=headers).content.decode())['data']
    fxlevel = ['高风险', '中风险']
    data = {
        'code': 200,
        'data': []
    }
    for i in range(len(resdata)):
        tt = i
        res = resdata[i]['dangerPros']
        x = []
        for i in range(len(res)):
            for j in res[i]["dangerAreas"]:
                x.append({
                    "provinceName": res[i]["provinceShortName"],
                    "cityName": j["cityName"],
                    "areaName": j["areaName"],
                })

        df = pd.DataFrame(x)
        df['全称'] = df['provinceName'] + df['cityName'] + df['areaName']
        df['address'] = df['provinceName'] + df['cityName']
        data['data'].append({'风险等级': fxlevel[tt], '数量': len(df), '地区': []})

        for i in range(len(df)):
            data['data'][tt]['地区'].append(df.iloc[i]['全称'])


        q = {
            "name": fxlevel[tt],
            "children": []
        }

        provinceName = df.drop_duplicates(subset=['address'], keep='first')

        for i in provinceName['address']:
            t = df[df['address'] == i]
            cd = len(t)
            q['children'].append({
                "name": f'{i}({cd})',
                "children": []
            })

            for kk in t['areaName']:
                for k in range(len(q['children'])):
                    if(q['children'][k]['name'] == f'{i}({cd})'):
                        q['children'][k]['children'].append({
                            'name': kk
                        })

        with open(f'demo/data/{fxlevel[tt]}.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(q, ensure_ascii=False, indent=4))
    with open(f'demo/data/风险地区.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False, indent=4))

# 近2个月中国疫情情况
def Moon_Tow_Near():
    url = 'https://api.inews.qq.com/newsqa/v1/query/inner/publish/modules/list?modules=chinaDayList,chinaDayAddList,nowConfirmStatis,provinceCompare'
    data = json.loads(requests.post(url, headers=headers).content.decode())['data']
    res = data['chinaDayAddList']
    res1 = data['chinaDayList']

    df = pd.DataFrame(res)
    df1 = pd.DataFrame(res1)

    def funx(x):
        if len(x) == 3 or (len(x.split('.')[0]) == 2 and len(x) == 4):
            x = x + '0'
        return x
    t = [df, df1]
    for i in t:
        x = i['y'].astype('str') + '.'
        y = (i['date'].astype('str'))
        y = y.apply(lambda x: funx(x))
        i['dateId'] = x + y
        i['dateId'] = pd.DatetimeIndex(i['dateId']).astype('str')

    pd.DataFrame(df).to_csv('demo/csv/近2个月新增情况.csv', encoding='utf-8', index=False)
    pd.DataFrame(df1).to_csv('demo/csv/近2个月累计情况.csv', encoding='utf-8', index=False)
    pd.DataFrame(df).to_sql('j2yxz', if_exists='replace', con=con, index=False)
    con.execute('ALTER TABLE j2yxz ADD id INT(16) NOT NULL PRIMARY KEY AUTO_INCREMENT FIRST;') # 添加自增字段id
    pd.DataFrame(df1).to_sql('j2ylj', if_exists='replace', con=con, index=False)
    con.execute('ALTER TABLE j2ylj ADD id INT(16) NOT NULL PRIMARY KEY AUTO_INCREMENT FIRST;') # 添加自增字段id

if __name__ == '__main__':
    pass
    # print('正在获取历史数据...')
    # lishishuju()  # 历史数据
    # print('正在获取中国今日疫情情况...')
    # yqday()  # 中国今日疫情情况
    # print('正在获取中国每日疫情...')
    # yqveryday()  # 中国每日疫情
    # print('正在获取实时热点...')
    # ssrd()  # 实时热点
    # print('正在获取国内各省目前疫情...')
    # parse()  # 国内各省目前疫情
    # print('正在获取国内风险地区...')
    # fxdq()  # 国内风险地区
    # print('正在获取进两月份的疫情趋势...')
    # Moon_Tow_Near()
    # print('获取完毕数据已更新!')
