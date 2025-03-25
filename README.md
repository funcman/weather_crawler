# 天气爬虫 (Weather Crawler)

这是一个天气数据爬虫程序，用于抓取实时天气数据（主要是气温）并将数据保存到CSV文件中。爬虫会从不同的数据源获取数据，并分别保存到各自的CSV文件中。

## 项目结构

- `weather_crawler.py` - 主程序，调用各API模块获取天气数据
- `openweathermap_api.py` - OpenWeatherMap API模块
- `weatherapi_api.py` - WeatherAPI.com API模块
- `visualcrossing_api.py` - Visual Crossing Weather API模块
- `data/` - 存放CSV数据文件的目录
- `requirements.txt` - 项目依赖
- `Dockerfile` - Docker镜像构建文件
- `docker-compose.yml` - Docker Compose配置文件

## 编码说明

本项目所有文件均使用**UTF-8**编码，包括：
- 所有Python源代码文件
- 生成的CSV数据文件
- 日志文件
- 配置文件

确保您的编辑器设置为UTF-8编码以正确查看和编辑项目文件。

## 功能特点

- 模块化设计，每个API都有独立的模块
- 单次运行，获取最新的天气数据后退出
- 支持通过城市名称或经纬度坐标获取数据
- 同时从多个数据源获取数据
- 将数据保存为CSV格式，方便后续分析
- 自动记录日志，便于监控和调试
- 支持Docker容器化部署，包括单次运行和定时任务模式
- 利用Python 3.10+特性，包括类型注解和结构模式匹配

## 安装步骤

### 常规安装

1. 克隆或下载此仓库
2. 安装依赖库：

```bash
pip install -r requirements.txt
```

3. 获取API密钥：
   - OpenWeatherMap: [https://openweathermap.org/api](https://openweathermap.org/api)
   - WeatherAPI: [https://www.weatherapi.com/](https://www.weatherapi.com/)
   - Visual Crossing Weather: [https://www.visualcrossing.com/](https://www.visualcrossing.com/)
4. 将获取的API密钥添加到`.env`文件中

### Docker安装

1. 克隆或下载此仓库
2. 编辑`.env`文件，设置API密钥
3. 使用Docker Compose构建和运行容器

## 配置

编辑`.env`文件，设置以下参数：

```
# OpenWeatherMap API密钥
API_KEY=your_openweathermap_key_here

# WeatherAPI.com API密钥
WEATHERAPI_KEY=your_weatherapi_key_here

# Visual Crossing Weather API密钥
VISUALCROSSING_KEY=your_visualcrossing_key_here

# 城市名称（默认为北京）
CITY=Beijing

# 可选：使用经纬度坐标替代城市名称
# LAT=39.9042
# LON=116.4074
```

## 使用方法

### 常规运行

运行脚本即可获取天气数据：

```bash
python weather_crawler.py
```

爬虫会从各个数据源抓取数据，然后将数据分别保存到不同的CSV文件中。运行完成后会立即退出。

### Docker运行

项目提供了两种Docker运行模式：

#### 1. 单次运行模式

运行一次爬虫后退出容器：

```bash
docker-compose run --rm weather-crawler
```

#### 2. 定时任务模式

以后台守护进程方式运行，每小时自动执行一次爬虫：

```bash
docker-compose up -d weather-crawler-cron
```

查看日志：
```bash
docker logs weather-crawler-cron
```

停止定时任务：
```bash
docker-compose down
```

## 自动定时运行

### Windows（使用Task Scheduler）

1. 打开任务计划程序
2. 创建基本任务，设置为每小时运行一次
3. 操作中选择启动程序，然后选择Python解释器和脚本路径

### Linux/MacOS（使用Cron）

添加以下crontab条目使脚本每小时运行一次：

```
0 * * * * cd /path/to/weather_crawler && python weather_crawler.py
```

## 数据输出

程序会为每个API创建单独的CSV文件：

- `data/openweathermap_data.csv` - 存储OpenWeatherMap数据
- `data/weatherapi_data.csv` - 存储WeatherAPI数据
- `data/visualcrossing_data.csv` - 存储Visual Crossing Weather数据

每次运行时，程序会向这些文件追加新的数据行。如果文件不存在，程序会创建新文件并添加表头。

## 数据字段说明

CSV文件包含以下字段：

基本字段（所有API共有）：
- `timestamp`: 数据抓取时间戳
- `temperature`: 当前温度（摄氏度）
- `feels_like`: 体感温度（摄氏度）
- `humidity`: 湿度百分比
- `pressure`: 大气压力（百帕）
- `weather_condition`: 天气状况（英文）
- `weather_description`: 天气状况详细描述
- `wind_speed`: 风速（米/秒）
- `city`: 城市名称
- `country`: 国家代码
- `data_source`: 数据来源

Visual Crossing Weather API附加字段：
- `precipitation`: 降水量（毫米）
- `uv_index`: 紫外线指数
- `cloud_cover`: 云量百分比

## 扩展新的API

如果要添加新的天气数据源，只需按照以下步骤：

1. 创建一个新的Python模块文件（例如`newapi_api.py`）
2. 在模块中实现`get_weather_data()`函数，返回标准格式的天气数据字典
3. 定义CSV文件路径作为模块变量 `CSV_FILE`
4. 在`weather_crawler.py`中导入该模块并添加相应的调用代码
5. 更新Dockerfile，添加新的模块文件复制

## 注意事项

- 免费API有调用频率限制，请勿过于频繁地调用
- API密钥请妥善保管，不要公开分享
- 使用Docker运行时，数据文件将保存在宿主机的`./data`目录中
- 本项目要求Python 3.10或更高版本，利用了结构模式匹配等新特性 