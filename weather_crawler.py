#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
天气爬虫主程序
独立调用不同的API模块获取天气数据并保存到各自的CSV文件

注意：本项目所有文件均使用UTF-8编码
要求Python版本 >= 3.10
"""

import os
import sys
import csv
import pandas as pd
import logging
import traceback
from typing import Dict, Any, Optional, Union, Literal
from dotenv import load_dotenv
from pathlib import Path

# 检查Python版本
if sys.version_info < (3, 10):
    raise RuntimeError("此程序需要Python 3.10或更高版本")

# 检查pandas和numpy版本
try:
    import pandas as pd
    import numpy as np
    print(f"pandas版本: {pd.__version__}")
    print(f"numpy版本: {np.__version__}")
except ImportError as e:
    print(f"警告: 无法导入pandas或numpy: {e}")
    # 使用csv模块作为备选
    import csv
    
# 导入各API模块
try:
    import openweathermap_api
    import weatherapi_api
    import visualcrossing_api
except ImportError as e:
    print(f"错误: 无法导入API模块: {e}")
    sys.exit(1)

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("weather_crawler.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 加载环境变量
load_dotenv()

# 确保数据目录存在
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

# 天气数据类型
WeatherData = Dict[str, Any]

def save_to_csv(data: Optional[WeatherData], csv_file: Union[str, Path]) -> bool:
    """
    将天气数据保存到CSV文件（使用UTF-8编码）
    
    Args:
        data: 天气数据字典，如果为None则不保存
        csv_file: CSV文件路径
        
    Returns:
        bool: 保存是否成功
    """
    if not data:
        return False
    
    try:
        csv_path = Path(csv_file)
        file_exists = csv_path.exists()
        
        try:
            # 尝试使用pandas
            df = pd.DataFrame([data])
            df.to_csv(csv_file, mode='a', header=not file_exists, index=False, encoding='utf-8')
        except Exception as pandas_error:
            logger.warning(f"Pandas保存失败，使用CSV模块保存: {str(pandas_error)}")
            
            # 使用CSV模块作为备选
            with open(csv_file, mode='a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=data.keys())
                if not file_exists:
                    writer.writeheader()
                writer.writerow(data)
        
        logger.info(f"数据已保存到 {csv_file}")
        return True
    except Exception as e:
        logger.error(f"保存数据时出错: {str(e)}")
        logger.error(traceback.format_exc())
        return False

def crawl_weather() -> None:
    """
    主爬虫函数，调用各API模块获取并保存天气数据
    """
    logger.info("开始抓取天气数据...")
    
    try:
        # 使用Python 3.10的结构模式匹配处理API结果
        # 调用OpenWeatherMap API
        match openweathermap_api.get_weather_data():
            case data if data is not None:
                if save_to_csv(data, openweathermap_api.CSV_FILE):
                    logger.info(f"成功抓取OpenWeatherMap数据，城市: {data.get('city')}，当前温度: {data['temperature']}°C")
            case _:
                logger.warning("未能获取OpenWeatherMap数据")
    except Exception as e:
        logger.error(f"处理OpenWeatherMap数据时出错: {str(e)}")
        logger.error(traceback.format_exc())
    
    try:
        # 调用WeatherAPI
        match weatherapi_api.get_weather_data():
            case data if data is not None:
                if save_to_csv(data, weatherapi_api.CSV_FILE):
                    logger.info(f"成功抓取WeatherAPI数据，城市: {data.get('city')}，当前温度: {data['temperature']}°C")
            case _:
                logger.warning("未能获取WeatherAPI数据")
    except Exception as e:
        logger.error(f"处理WeatherAPI数据时出错: {str(e)}")
        logger.error(traceback.format_exc())
        
    try:
        # 调用Visual Crossing Weather API
        match visualcrossing_api.get_weather_data():
            case data if data is not None:
                if save_to_csv(data, visualcrossing_api.CSV_FILE):
                    logger.info(f"成功抓取Visual Crossing数据，城市: {data.get('city')}，当前温度: {data['temperature']}°C")
                    if 'precipitation' in data:
                        logger.info(f"降水量: {data['precipitation']}mm, 紫外线指数: {data.get('uv_index', 0)}")
            case _:
                logger.warning("未能获取Visual Crossing天气数据")
    except Exception as e:
        logger.error(f"处理Visual Crossing数据时出错: {str(e)}")
        logger.error(traceback.format_exc())

def main() -> None:
    """
    主函数，只运行一次爬虫然后退出
    """
    try:
        logger.info(f"天气爬虫启动... (Python {sys.version.split(' ')[0]})")
        
        # 运行一次爬虫
        crawl_weather()
        
        logger.info("天气爬虫运行完毕，已退出")
    except Exception as e:
        logger.critical(f"爬虫运行异常: {str(e)}")
        logger.critical(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    main() 