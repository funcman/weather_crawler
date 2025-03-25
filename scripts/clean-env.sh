#!/bin/bash

# 替换API密钥为占位符
sed 's/API_KEY=.*/API_KEY=your_openweathermap_api_key_here/' |
sed 's/WEATHERAPI_KEY=.*/WEATHERAPI_KEY=your_weatherapi_key_here/' |
sed 's/VISUALCROSSING_KEY=.*/VISUALCROSSING_KEY=your_visualcrossing_key_here/' 