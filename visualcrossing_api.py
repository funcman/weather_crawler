#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Visual Crossing Weather API 天气数据源模块
提供从Visual Crossing Weather获取天气数据的接口

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
    precipitation: float  # 降水量
    uv_index: float      # 紫外线指数
    cloud_cover: int     # 云量

def get_weather_condition_description(condition: str) -> str:
    """
    根据天气状况返回中文描述
    
    Args:
        condition: 天气状况原始描述
        
    Returns:
        str: 中文天气描述
    """
    condition_lower = condition.lower()
    
    if "rain" in condition_lower:
        return "降雨"
    elif "snow" in condition_lower:
        return "降雪"
    elif "cloud" in condition_lower or "overcast" in condition_lower:
        return "多云"
    elif "clear" in condition_lower or "sunny" in condition_lower:
        return "晴朗"
    elif "fog" in condition_lower or "mist" in condition_lower:
        return "雾"
    elif "thunder" in condition_lower or "storm" in condition_lower:
        return "雷暴"
    else:
        return condition  # 保持原始描述

def get_weather_data() -> Optional[WeatherData]:
    """
    从Visual Crossing Weather获取天气数据
    需要在.env中添加VISUALCROSSING_KEY
    返回包含天气信息的字典（UTF-8编码）
    
    Returns:
        Optional[WeatherData]: 天气数据字典或None（如果获取失败）
    """
    try:
        api_key: Final = os.getenv("VISUALCROSSING_KEY", "")
        if not api_key:
            logger.error("未设置VISUALCROSSING_KEY环境变量")
            return None
            
        # 获取位置信息，优先使用坐标
        city: Final = os.getenv("CITY", "Beijing")
        lat: Final = os.getenv("LAT")
        lon: Final = os.getenv("LON")
        
        # 使用Python 3.10的结构模式匹配选择位置参数
        location: str = ""
        match (lat, lon):
            case (str(lat_val), str(lon_val)) if lat_val and lon_val:
                location = f"{lat_val},{lon_val}"
            case _:
                location = city
                
        # 构建API URL
        url: Final = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}/today"
        
        params = {
            "unitGroup": "metric",
            "include": "current",
            "key": api_key,
            "contentType": "json"
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # 使用结构模式匹配处理返回数据
        match data:
            case {"currentConditions": current, "address": address, "days": [today, *_]} if current:
                # 处理天气状况描述
                weather_condition = current.get("conditions", "")
                weather_description = get_weather_condition_description(weather_condition)
                
                # 汇总数据
                return WeatherData(
                    timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    temperature=current.get("temp", 0.0),
                    feels_like=current.get("feelslike", 0.0),
                    humidity=current.get("humidity", 0),
                    pressure=current.get("pressure", 0.0),
                    weather_condition=weather_condition,
                    weather_description=weather_description,
                    wind_speed=current.get("windspeed", 0.0) / 3.6,  # 转换为m/s
                    city=address,
                    country=data.get("resolvedAddress", "").split(",")[-1].strip() if "," in data.get("resolvedAddress", "") else "",
                    data_source="VisualCrossing",
                    precipitation=current.get("precip", 0.0),
                    uv_index=current.get("uvindex", 0.0),
                    cloud_cover=current.get("cloudcover", 0)
                )
            case _:
                logger.error("无法解析Visual Crossing天气数据")
                return None
                
    except Exception as e:
        logger.error(f"从Visual Crossing获取数据出错: {str(e)}")
        return None

# 文件输出路径
CSV_FILE: Final = Path("data") / "visualcrossing_data.csv"

if __name__ == "__main__":
    # 设置日志记录
    logging.basicConfig(level=logging.INFO)
    
    # 测试API
    match get_weather_data():
        case data if data is not None:
            print(f"当前温度: {data['temperature']}°C")
            print(f"天气状况: {data['weather_condition']}")
            print(f"降水量: {data.get('precipitation', 0)}mm")
            print(f"紫外线指数: {data.get('uv_index', 0)}")
        case _:
            print("无法获取天气数据") 