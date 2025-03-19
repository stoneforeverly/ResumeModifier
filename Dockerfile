# 使用官方 Python 3.9 镜像
FROM python:3.9

# 设置工作目录
WORKDIR /app

# 复制依赖文件 requirements.txt（这样可以利用 Docker 缓存）
COPY requirements.txt .

# 先安装依赖（避免频繁复制所有代码时重复安装）
RUN pip install --no-cache-dir -r requirements.txt

# 复制当前目录所有文件到 /app
COPY . .

# 设置 PYTHONPATH，确保 Flask 能正确导入 app 目录
ENV PYTHONPATH=/app

# 公开 Flask 运行的端口
EXPOSE 5000

# 运行 Flask 应用
CMD ["python", "run.py"]
