#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
WeatherAPI.com 天气数据源模块
提供从WeatherAPI.com获取天气数据的接口

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
    pressure: float
    weather_condition: str
    weather_description: str
    wind_speed: float
    city: str
    country: str
    data_source: str

def get_weather_data() -> Optional[WeatherData]:
    """
    从WeatherAPI.com获取天气数据
    需要在.env中添加WEATHERAPI_KEY
    返回包含天气信息的字典（UTF-8编码）
    
    Returns:
        Optional[WeatherData]: 天气数据字典或None（如果获取失败）
    """
    try:
        api_key: Final = os.getenv("WEATHERAPI_KEY", "")
        if not api_key:
            logger.error("未设置WEATHERAPI_KEY环境变量")
            return None
            
        city: Final = os.getenv("CITY", "Beijing")
        url: Final = f"https://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&aqi=no&lang=zh"
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # 使用字典解包构造返回值
        return WeatherData(
            timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            temperature=data["current"]["temp_c"],
            feels_like=data["current"]["feelslike_c"],
            humidity=data["current"]["humidity"],
            pressure=data["current"]["pressure_mb"],
            weather_condition=data["current"]["condition"]["text"],
            weather_description=data["current"]["condition"]["text"],
            wind_speed=data["current"]["wind_kph"] / 3.6,  # 转换为m/s
            city=data["location"]["name"],
            country=data["location"]["country"],
            data_source="WeatherAPI"
        )
    except Exception as e:
        logger.error(f"从WeatherAPI获取数据出错: {str(e)}")
        return None

# 文件输出路径
CSV_FILE: Final = Path("data") / "weatherapi_data.csv"

if __name__ == "__main__":
    # 设置日志记录
    logging.basicConfig(level=logging.INFO)
    
    # 测试API
    match get_weather_data():
        case data if data is not None:
            print(f"当前温度: {data['temperature']}°C")
            print(f"天气状况: {data['weather_condition']}")
        case _:
            print("无法获取天气数据") 