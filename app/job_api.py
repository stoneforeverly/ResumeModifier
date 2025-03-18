import sys
import os
from flask import Blueprint, jsonify, request
import requests
from app.database import collection  # 确保正确导入 MongoDB 连接

sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/.."))  # 确保 `app` 目录在路径里


job_api = Blueprint("job_api", __name__)

API_URL = "https://jsearch.p.rapidapi.com/search"
HEADERS = {
    "X-RapidAPI-Host": "jsearch.p.rapidapi.com",
    "X-RapidAPI-Key": "eaa381d7f1msh6d53c9dad8ab410p118824jsneb2763f234dd"
}

def fetch_and_store_jobs(query="developer", location=None, max_pages=3, remote_only=None, min_salary=None, date_posted=None):
    print("🚀 Fetching jobs with filters...")

    all_jobs = []
    for page in range(1, max_pages + 1):
        print(f"📡 Fetching page {page}...")

        # 构造请求参数
        params = {
            "query": query,
            "num_pages": page,  # 控制获取多少页数据
        }

        if location:  # 只有用户提供了 location，才加进去
            params["location"] = location

        if remote_only is not None:  # 允许 False 值，所以要用 `is not None` 判断
            params["remote_jobs_only"] = str(remote_only).lower()

        if min_salary:  # 只有提供了最小薪资才过滤
            params["salary_min"] = min_salary

        if date_posted:  # 只过滤有时间要求的
            params["date_posted"] = date_posted

        # 发送 API 请求
        response = requests.get(API_URL, headers=HEADERS, params=params)
        print(f"📡 API response code: {response.status_code}")

        if response.status_code == 200:
            jobs_data = response.json().get("data", [])
            if not jobs_data:
                print("⚠️ No more job data available, stopping fetch.")
                break

            print(f"✅ Page {page} - {len(jobs_data)} job postings received")

            for job in jobs_data:
                job_record = {
                    "title": job.get("job_title", "N/A"),
                    "company": job.get("employer_name", "N/A"),
                    "location": job.get("job_location", "N/A"),
                    "salary": job.get("job_salary", "N/A"),
                    "apply_link": job.get("job_apply_link", "N/A"),
                    "posted_at": job.get("job_posted_at", "N/A"),
                    "job_description": job.get("job_description", "N/A")  # 新增 JD
                }

                if not collection.find_one({"apply_link": job_record["apply_link"]}):
                    collection.insert_one(job_record)
                    print(f"📌 Stored job: {job_record['title']} - {job_record['company']}")

        else:
            print(f"❌ API request failed at page {page}, stopping fetch.")
            break

    print("🎯 Data successfully stored in MongoDB")




# ✅ 提供 API 端点，让前端调用这个函数
@job_api.route("/fetch_jobs", methods=["GET"])
def fetch_jobs_endpoint():
    query = request.args.get("query", "developer")
    location = request.args.get("location", None)
    max_pages = int(request.args.get("max_pages", 1))
    remote_only = request.args.get("remote_only", None)
    min_salary = request.args.get("min_salary", None)
    date_posted = request.args.get("date_posted", None)

    fetch_and_store_jobs(query, location, max_pages, remote_only, min_salary, date_posted)

    return jsonify({"message": "Job data fetching initiated"}), 200