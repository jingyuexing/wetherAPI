# Wether API

中国气象局数据API


```py
Wether(stationID=0, stationName="")     # Wether Class
```
如果清楚气象站id则直接填写id否则可以填写站点名,站点名可以查看[数据](data/stationsData.json)

```py
Wether().show(self,data=False)
```
显示数据 仅返回温度,风力,以及天气,`data`默认为False,若为真,则直接返回一个`dict`类型数据
反之直接输出
```
当前天气:
当前温度为:
当前风速及风向:
```

# LICENSE

[GNU GPL](LICENSE)
