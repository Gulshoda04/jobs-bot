import asyncio
import httpx

API_BASE_URL = "https://remoteok.com/api"

cache = {}


async def get_jobs(keyword: str, page: int = 1, retries: int = 3):
    cache_key = f"{keyword}_page{page}"
    if cache_key in cache:
        return cache[cache_key]

    attempt = 0
    while attempt < retries:
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(API_BASE_URL, params={"search": keyword, "page": page})

                if resp.status_code == 429:
                    wait_time = int(resp.headers.get("Retry-After", 1))
                    await asyncio.sleep(wait_time)
                    attempt += 1
                    continue

                resp.raise_for_status()
                data = resp.json()
                jobs = data or []
                cache[cache_key] = jobs  # save in cache
                return jobs
        except Exception as e:
            attempt += 1
            await asyncio.sleep(1)
    return []


async def get_job_by_id(job_id: str, retries: int = 3):
    if job_id in cache:
        return cache[job_id]

    attempt = 0
    while attempt < retries:
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(f"{API_BASE_URL}/{job_id}/")

                if resp.status_code == 429:
                    wait_time = int(resp.headers.get("Retry-After", 1))
                    await asyncio.sleep(wait_time)
                    attempt += 1
                    continue

                resp.raise_for_status()
                data = resp.json()
                cache[job_id] = data
                return data
        except Exception as e:
            attempt += 1
            await asyncio.sleep(1)
    return None


async def get_job_detail(job_id: str, retries: int = 3):
    return await get_job_by_id(job_id, retries)
