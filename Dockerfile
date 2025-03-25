# 使用Python 3.10作为基础镜像
FROM python:3.10-slim-bookworm

# 设置工作目录
WORKDIR /app

# 设置环境变量，确保Python使用UTF-8编码
ENV PYTHONIOENCODING=utf-8
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV TZ=Asia/Shanghai
ENV PYTHONUNBUFFERED=1

# 安装必要的系统包
RUN apt-get update && apt-get install -y \
    cron \
    tzdata \
    gcc \
    g++ \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# 创建数据和日志目录
RUN mkdir -p data logs

# 创建空的日志文件，确保tail命令正常工作
RUN touch /app/cron.log

# 复制依赖文件并安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir wheel && \
    pip install --no-cache-dir -r requirements.txt

# 验证安装的库版本
RUN pip list

# 复制项目文件到容器
COPY weather_crawler.py .
COPY openweathermap_api.py .
COPY weatherapi_api.py .
COPY visualcrossing_api.py .
COPY .env .
COPY README.md .
COPY test_python310.py .

# 为定时任务创建crontab文件
RUN echo "0 * * * * cd /app && python3 /app/weather_crawler.py >> /app/cron.log 2>&1" > /etc/cron.d/weather-cron
RUN chmod 0644 /etc/cron.d/weather-cron
RUN crontab /etc/cron.d/weather-cron

# 创建启动脚本
RUN echo '#!/bin/sh\n\
# 显示Python版本和库版本\n\
python3 --version\n\
pip list | grep -E "numpy|pandas"\n\
\n\
# 首先运行一次爬虫\n\
python3 /app/weather_crawler.py\n\
\n\
# 如果是定时模式，则启动cron守护进程并保持容器运行\n\
if [ "$1" = "cron" ]; then\n\
    echo "启动定时任务模式，每小时运行一次爬虫..."\n\
    cron\n\
    # 保持容器运行\n\
    tail -f /app/cron.log\n\
fi\n\
' > /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# 设置启动命令
ENTRYPOINT ["/app/entrypoint.sh"]

# 默认不启动cron，只运行一次爬虫
CMD ["once"] 