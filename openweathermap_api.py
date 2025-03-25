#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
OpenWeatherMap 天气数据源模块
提供从OpenWeatherMap获取天气数据的接口

注意：本模块使用UTF-8编码
要求Python版本 >= 3.10
"""

import os
import sys
import datetime
import requests
import logging
from typing import Dict, Any, Optional, TypedDict, Final
from dotenv import load_dotenv
from pathlib import Path

# 检查Python版本
if sys.version_info < (3, 10):
    raise RuntimeError("此模块需要Python 3.10或更高版本")

logger = logging.getLogger(__name__)

# 加载环境变量
load_dotenv()

# 定义天气数据结构
class WeatherData(TypedDict, total=False):
    timestamp: str
    temperature: float
    feels_like: float
    humidity: int
    pressure: int
    weather_condition: str
    
    weather_description: str
    wind_speed: float
    city: str
    country: str
    data_source: str

def get_weather_data() -> Optional[WeatherData]:
    """
    从OpenWeatherMap获取天气数据
    返回包含天气信息的字典（UTF-8编码）
    
    Returns:
        Optional[WeatherData]: 天气数据字典或None（如果获取失败）
    """
    try:
        api_key: Final = os.getenv("API_KEY", "")
        if not api_key:
            logger.error("未设置OpenWeatherMap API_KEY环境变量")
            return None
            
        city: Final = os.getenv("CITY", "Beijing")
        lat: Final = os.getenv("LAT")
        lon: Final = os.getenv("LON")
        
        base_url: Final = "https://api.openweathermap.org/data/2.5/weather"
        
        # 根据配置决定使用城市名称还是坐标
        params: Dict[str, Any] = {
            "appid": api_key,
            "units": "metric",  # 使用摄氏度
            "lang": "zh_cn"     # 使用中文
        }
        
        # 使用Python 3.10的结构模式匹配选择参数
        match (lat, lon):
            case (str(lat_val), str(lon_val)) if lat_val and lon_val:
                params.update({"lat": lat_val, "lon": lon_val})
            case _:
                params["q"] = city
        
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()  # 如果请求失败，抛出异常
        
        data = response.json()
        
        # 使用字典解包构造返回值
        return WeatherData(
            timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            temperature=data["main"]["temp"],
            feels_like=data["main"]["feels_like"],
            humidity=data["main"]["humidity"],
            pressure=data["main"]["pressure"],
            weather_condition=data["weather"][0]["main"],
            weather_description=data["weather"][0]["description"],
            wind_speed=data["wind"]["speed"],
            city=data["name"],
            country=data["sys"]["country"],
            data_source="OpenWeatherMap"
        )
    except Exception as e:
        logger.error(f"获取OpenWeatherMap天气数据时出错: {str(e)}")
        return None

# 文件输出路径
CSV_FILE: Final = Path("data") / "openweathermap_data.csv"

if __name__ == "__main__":
    # 设置日志记录
    logging.basicConfig(level=logging.INFO)
    
    # 测试API
    match get_weather_data():
        case data if data is not None:
            print(f"当前温度: {data['temperature']}°C")
            print(f"天气状况: {data['weather_condition']}")
            print(f"天气描述: {data['weather_description']} (中文)")
        case _:
            print("无法获取天气数据") 