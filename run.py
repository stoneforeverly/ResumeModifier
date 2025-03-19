from flask import Flask
from app.job_api import job_api  # 确保正确导入你的 API 蓝图

app = Flask(__name__)

# 注册蓝图
app.register_blueprint(job_api, url_prefix="/jobs")

if __name__ == "__main__":
        # 允许外部访问，并监听 5000 端口
    app.run(host="0.0.0.0", port=5000)
