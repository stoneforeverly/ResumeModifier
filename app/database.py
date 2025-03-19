from pymongo import MongoClient

# 连接本地 MongoDB
client = MongoClient("mongodb://host.docker.internal:27017/")

# 创建数据库和集合
db = client["jobSearch"]  # 数据库名称
collection = db["jobs"]  # 集合（类似 SQL 的表）




