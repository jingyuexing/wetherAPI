# -*- coding: utf-8 -*-
# @Author: Jingyuexing
# @Date:   2020-04-24 15:34:28
# @Last Modified by:   Jingyuexing
# @Last Modified time: 2022-06-14 22:59:59


class Wether:
    """
    Accept: application/json, text/javascript, */*; q=0.01
    Accept-Encoding: gzip, deflate
    Accept-Language: en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7
    Connection: keep-alive
    Content-Length: 15
    Content-Type: application/x-www-form-urlencoded; charset=UTF-8
    Cookie: pgv_pvi=8631199744; _pk_ses.6.a479=1; _pk_ses.1.a479=*; PHPSESSID=kfnm3ggvp3gade1afj180l5i65; pgv_si=s9177704448; Hm_lvt_d9508cf73ee2d3c3a3f628fe26bd31ab=1598146167,1598146577; _pk_testcookie.6.a479=1; _pk_id.1.a479=394e49a463074aa1.1598146168.1.1598146578.1598146168.; login_id_chat=0; login_name_chat=0; _pk_id.6.a479=8fa30b9ea92f19ae.1598146168.1.1598146578.1598146168.; Hm_lpvt_d9508cf73ee2d3c3a3f628fe26bd31ab=1598146586
    DNT: 1
    Host: api.data.cma.cn
    Origin: http://api.data.cma.cn
    Referer: http://api.data.cma.cn/forecast/index.html?t=57498
    User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36
    X-Requested-With: XMLHttpRequest
    """
    maxWindSpeed = 0  # 最大风速
    minWindSpeed = 0  # 最小风速
    windSpeed = 0  # 风速
    windDirection = 0  # 风向
    latitude = 0  # 纬度偏差
    longitude = 0  # 经度偏差
    temperature = 0  # 平均温度
    maxTemperature = 0  # 最高温度
    minTemperature = 0  # 最低温度
    maxTemperature12h = 0  # 12小时最高温度
    minTemperature12h = 0  # 12小时最低温度
    maxTemperature24h = 0  # 24小时最高温度
    minTemperature24h = 0  # 24小时最低温度
    humidity = 0  # 相对湿度
    pressure = 0  # 气压 百帕
    pressureSea = 0  # 海平面气压 百帕
    cloud = 0  # 总云量 百分率
    cloudLow = 0  # 低云量 百分率
    wether = 0  # 现在天气
    stationName = ""
    station = {}
    data = {}
    """docstring for Wether"""

    def __init__(self, stationID=0, stationName=""):
        self.station = self.loadData("data/stationsData.json")
        url = "http://data.cma.cn/weatherGis/web/weather/weatherFcst/getSevenDayData"
        if(stationID != 0):
            self.data = self.request(url, param={
                "staIds": stationID
            })
        elif(stationName != ''):
            stationID = self.find(stationName)
            self.data = self.request(url, param={
                "staIds": stationID
            })

    def find(self, stationName="北京"):
        index = self.station.keys()
        for x in index:
            if(stationName in self.station[x]["station"]):
                indexId = x
        return indexId

    def loadData(self, fileName):
        import json
        data = {}
        if type(fileName) == str:
           with open(fileName,mode='r',encoding='utf-8') as file:
            data = json.load(file)
        return data

    def getDayNigntData(self):
        pass

    def parserData(self, index=0):
        if(self.data):
            data = self.data["list"][index]
            self.cloud = data['clo_Cov']
            self.cloudLow = data['clo_Cov_Low']
            self.latitude = data['lat']
            self.wether = data['wep']
            self.maxTemperature24h = data['tem_Max_24h']
            self.minTemperature24h = data['tem_Min_24h']
            self.temperature = data['tem']
            self.windSpeed = data['win_S']
            self.windDirection = data['win_D']
        else:
            raise Exception("API ERROR")

    def request(self, url='', param={}, method="GET"):
        import urllib3
        import json
        header = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cache-Control": "max-age=0",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
            "Connection": "keep-alive",
            "DNT": "1",
            "Accept": "application/json, text/plain, */*",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"
        }
        http = urllib3.PoolManager()
        req = http.request(method=method, url=url,
                           fields=param, headers=header)
        if (req.status == 200):
            return json.loads(req.data.decode("utf-8"), encoding='utf-8')

    def windDri(self):
        """风向

        [description]

        Returns:
            [type] -- [description]
        """
        win = ""
        if(0 < self.windDirection < 45):
            win = "北偏东"
        elif(45 < self.windDirection < 90):
            win = "东偏北"
        elif(90 < self.windDirection < 135):
            win = "东偏南"
        elif(135 < self.windDirection < 180):
            win = "南偏东"
        elif(180 < self.windDirection < 225):
            win = "南偏西"
        elif(225 < self.windDirection < 270):
            win = "南偏南"
        elif(270 < self.windDirection < 315):
            win = "西偏北"
        elif(315 < self.windDirection < 360):
            win = "北偏西"
        return win

    def winSpeed(self):
        """风速等级

        [description]

        Returns:
            str -- 等级
        """
        winLevel = ""
        if(self.windSpeed <= 0.2):
            winLevel = "微风"
        elif(0.2 < self.windSpeed <= 1.5):
            winLevel = "1级"
        elif(1.5 < self.windSpeed <= 3.3):
            winLevel = "2级"
        elif(3.3 < self.windSpeed <= 5.4):
            winLevel = "3级"
        elif(5.4 < self.windSpeed <= 7.9):
            winLevel = "4级"
        elif(7.9 < self.windSpeed <= 10.7):
            winLevel = "5级"
        elif(10.7 < self.windSpeed <= 13.8):
            winLevel = "6级"
        elif(13.8 < self.windSpeed <= 17.1):
            winLevel = "7级"
        elif(17.1 < self.windSpeed <= 20.7):
            winLevel = "8级"
        elif(20.7 < self.windSpeed <= 24.4):
            winLevel = "9级"
        elif(24.4 < self.windSpeed <= 28.4):
            winLevel = "10级"
        elif(28.4 < self.windSpeed <= 32.6):
            winLevel = "11级"
        elif(32.6 < self.windSpeed <= 132):
            winLevel = "12级以上"
        return winLevel
    def wetherNow(self):
        wetherList = [
            "晴☀",
            "多云🌥",
            "阴⛅",
            "阵雨",
            "雷阵雨⛈",
            "雷阵雨伴有冰雹",
            "雨夹雪",
            "小雨",
            "中雨",
            "大雨🌧",
            "暴雨",
            "大暴雨",
            "特大暴雨",
            "阵雪",
            "小雪❄",
            "中雪❄❄",
            "大雪❄❄❄",
            "暴雪❄❄❄❄",
            "雾",
            "冻雨",
            "沙尘暴",
            "小到中雨",
            "中到大雨",
            "大到暴雨",
            "暴雨到大暴雨",
            "大暴雨到特大暴雨",
            "小到中雪",
            "中到大雪",
            "大到暴雪",
            "浮尘",
            "扬沙",
            "强沙尘暴",
            "霾"
        ]
        return wetherList[int(self.wether)]

    def show(self,data=False):
        self.parserData()
        if(data):
            return {
                "wether":self.wetherNow(),
                "tem":self.temperature,
                "wind":self.windDri(),
                "windspeed":self.winSpeed()
                }
        else:
            print("""当前天气:%s   \n当前温度为:%s  \n当前风速及风向:%s""" % (self.wetherNow(), self.temperature, self.windDri() + self.winSpeed()))


if __name__ == '__main__':
    import argparse
    parse = argparse.ArgumentParser("查询天气")
    parse.add_argument("--locale","-l",type=str,help="查询的地区,比如:北京")
    arg = parse.parse_args()
    if(arg.locale):
        w =  Wether(stationName=arg.locale)
        print(f"{arg.locale}的天气如下:")
        w.show(False)
