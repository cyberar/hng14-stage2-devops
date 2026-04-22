from fastapi import FastAPI, HTTPException
from pydantic_settings import BaseSettings, SettingsConfigDict
import redis
import uuid


app = FastAPI() 

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    
    redis_host: str 
    redis_port: int 
    redis_username: str
    redis_password: str

settings = Settings()

r = redis.Redis(host=settings.redis_host,
                port=settings.redis_port,
                username=settings.redis_username,
                password=settings.redis_password)  # remove hardcoded connection details

@app.post("/jobs")
def create_job():
    job_id = str(uuid.uuid4())
    r.lpush("job", job_id)
    r.hset(f"job:{job_id}", "status", "queued")
    return {"job_id": job_id}

@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    status = r.hget(f"job:{job_id}", "status")
    if not status:
        raise HTTPException(status_code=404, detail="Job not found") # return a http exception error if job is not found
    return {"job_id": job_id, "status": status.decode()}
    
@app.get("/health")
def health_check():
    return {"status": "API is healthy"}