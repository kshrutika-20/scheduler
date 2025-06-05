from src.services.scheduler import SchedulerService
from config import ADAPTER_CONFIGS, TRANSFORMATION_API_URL, EXECUTION_MODE
from src.services.executor import get_executor
from src.services.transformer import Transformer

if __name__ == "__main__":
    executor = get_executor(EXECUTION_MODE)
    transformer = Transformer(TRANSFORMATION_API_URL, executor)
    scheduler = SchedulerService(transformer, executor)
    scheduler.load_jobs(ADAPTER_CONFIGS)
    scheduler.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        scheduler.stop()