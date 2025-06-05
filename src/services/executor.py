from src.services.parallel_executor import ParallelExecutor
from src.services.celery_executor import CeleryExecutor

def get_executor(mode="thread"):
    if mode == "celery":
        return CeleryExecutor()
    return ParallelExecutor()