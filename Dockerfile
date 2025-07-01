# 使用Python官方轻量镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=production

# 安装系统依赖（最小化安装）
RUN apt-get update && apt-get install -y \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 复制requirements文件并安装Python依赖
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY HCF_Prediction/pythonProject2/ ./

# 确保模型文件存在
RUN ls -la *.pkl || echo "警告：未找到模型文件"

# 暴露端口（Railway/Render会动态分配）
EXPOSE 5000

# 启动应用（支持动态端口）
CMD ["python", "app.py"] 