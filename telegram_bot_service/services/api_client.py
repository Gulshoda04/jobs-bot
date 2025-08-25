import requests
from config import API_URL

# services/api_client.py
import httpx

API_BASE_URL = "https://remoteok.com/api"

async def get_jobs(keyword, page=1):
    async with httpx.AsyncClient() as client:
        resp = await client.get(API_BASE_URL, params={"search": keyword, "page": page})
        if resp.status_code == 200:
            data = resp.json()
            return data or []
        return []



# def search_jobs(query, page=1):
#     resp = requests.get(API_URL, params={"search": query, "page": page})
#     if resp.status_code == 200:
#         return resp.json()
#     return []

async def get_job_detail(job_id):
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{API_URL}{job_id}/")
        if resp.status_code == 200:
            return resp.json()
        return None
