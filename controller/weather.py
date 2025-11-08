# -*- coding: utf-8 -*-
# @Time   : 2025/1/15 20:04
# @Author : WWEE
# @File   : weather.py
import requests


class weather:
    def __init__(self):
        key = "3dcea51c39f6c84bac3d50356cc9f39f"
        city = "350121"
        extensions = "all"
        output = "JSON"
        self.url = f"https://restapi.amap.com/v3/weather/weatherInfo?key={key}&city={city}&extensions={extensions}&output={output}"

    def get_weather(self):
        try:
            response = requests.get(self.url)
            if response.status_code == 200:
                result = response.json()
                forecasts = result.get("forecasts", [])
                if forecasts:
                    city = forecasts[0].get("city")
                    print(f"城市: {forecasts[0].get('city')}")
                    print(f"报告时间: {forecasts[0].get('reporttime')}")
                    casts = forecasts[0].get("casts", [])
                    for cast in casts:
                        print(f"日期: {cast.get('date')}, 周: {cast.get('week')}")
                        print(
                            f"  白天天气: {cast.get('dayweather')}, 白天温度: {cast.get('daytemp')}°C, 白天风向: {cast.get('daywind')}, 白天风力: {cast.get('daypower')}")
                        print(
                            f"  夜间天气: {cast.get('nightweather')}, 夜间温度: {cast.get('nighttemp')}°C, 夜间风向: {cast.get('nightwind')}, 夜间风力: {cast.get('nightpower')}")
                        return cast, city
            else:
                print(f"请求失败，状态码: {response.status_code}")
        except requests.RequestException as e:
            print(f"请求异常: {e}")

if __name__ == "__main__":
    m = weather()
    m.get_weather()


