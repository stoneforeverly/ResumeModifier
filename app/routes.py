from flask import Blueprint, jsonify
from app.database import collection

api = Blueprint("api", __name__)

@api.route("/jobs", methods=["GET"])
def get_jobs():
    jobs = list(collection.find({}, {"_id": 0}))  # 返回所有 job，不包含 MongoDB 的 _id 字段
    return jsonify(jobs)