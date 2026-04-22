import redis
import time
import os
import signal
import dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

dotenv.load_dotenv()

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

# r = redis.Redis(host=os.getenv("REDIS_HOST"), 
#                 port=int(os.getenv("REDIS_PORT", 13248)))  # remove hardcoded connection details

def process_job(job_id):
    print(f"Processing job {job_id}")
    time.sleep(2)  # simulate work
    r.hset(f"job:{job_id}", "status", "completed")
    print(f"Done: {job_id}")

while True:
    job = r.brpop("job", timeout=5)
    if job:
        _, job_id = job
        process_job(job_id.decode())