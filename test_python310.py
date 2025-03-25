#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Python 3.10 特性测试脚本
用于验证项目在Python 3.10环境下正确运行
"""

import sys
import platform
from typing import Any, Optional

def check_python_version() -> None:
    """检查Python版本，确保是3.10或更高版本"""
    print(f"Python版本: {sys.version}")
    if sys.version_info < (3, 10):
        print("警告: 此项目需要Python 3.10或更高版本")
    else:
        print("✓ Python版本满足要求")

def test_match_case() -> None:
    """测试结构模式匹配（Python 3.10新特性）"""
    print("\n测试结构模式匹配:")
    
    def get_weather_description(weather_code: int) -> str:
        """使用结构模式匹配获取天气描述"""
        match weather_code:
            case code if 200 <= code < 300:
                return "雷雨"
            case code if 300 <= code < 400:
                return "毛毛雨"
            case code if 500 <= code < 600:
                return "雨"
            case code if 600 <= code < 700:
                return "雪"
            case code if 700 <= code < 800:
                return "雾"
            case 800:
                return "晴"
            case code if 801 <= code < 900:
                return "多云"
            case _:
                return "未知天气"
    
    test_codes = [202, 350, 503, 601, 741, 800, 802, 999]
    for code in test_codes:
        print(f"天气代码 {code}: {get_weather_description(code)}")
    
    # 测试更复杂的模式匹配
    print("\n复杂模式匹配测试:")
    
    def parse_location(location: tuple[Any, ...]) -> str:
        match location:
            case (str(city), str(country)):
                return f"{city}, {country}"
            case (float(lat), float(lon)):
                return f"纬度: {lat}, 经度: {lon}"
            case (str(city), int(zipcode)):
                return f"{city}, 邮编: {zipcode}"
            case _:
                return "未知位置格式"
    
    test_locations = [
        ("北京", "中国"),
        (39.9042, 116.4074),
        ("上海", 200000),
        (123, "无效")
    ]
    
    for loc in test_locations:
        print(f"位置 {loc}: {parse_location(loc)}")

def test_union_types() -> None:
    """测试Python 3.10中改进的Union类型语法"""
    print("\n测试Union类型简化语法:")
    
    # Python 3.10允许使用 X | Y 代替 Union[X, Y]
    def process_data(data: dict[str, str | int | float | None]) -> None:
        for key, value in data.items():
            print(f"键: {key}, 值: {value}, 类型: {type(value).__name__}")
    
    test_data = {
        "city": "北京",
        "temperature": 25.5,
        "humidity": 65,
        "precipitation": None
    }
    
    process_data(test_data)

def main() -> None:
    """主函数"""
    print("Python 3.10 特性测试\n" + "="*20)
    check_python_version()
    test_match_case()
    test_union_types()
    print("\n所有测试完成")

if __name__ == "__main__":
    main() 