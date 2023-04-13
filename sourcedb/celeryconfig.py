import os

celery_broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery_result_backend = os.environ.get(
    "CELERY_RESULT_BACKEND", "redis://localhost:6379"
)

without_heartbeat = True
without_gossip = True
task_acks_late = True
concurrency = 4
worker_prefetch_multiplier = 1
autoscale = 10, 3
