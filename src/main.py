from factories.adapter_factory import AdapterFactory
from services.transformer import Transformer
from services.parallel_executor import ParallelExecutor
from services.scheduler import Scheduler
from config import ADAPTER_CONFIGS, TRANSFORMATION_API_URL
import time

def poll_and_transform(adapter, transformer):
  records = adapter.fetch_records()
  if not records:
    print("No unprocessed data found")
    return

  results = transformer.transform_records(records)
  successful = [record for record, success in zip(records, results) if success]

  if successful:
    adapter.post_process(successful)
    print(f"Marked {len(successful)} records as processed")
  else:
    print("No records were successfully transformed")

if __name__ == "__main__":
  parallel_executor = ParallelExecutor(max_workers=4)
  transformer = Transformer(transformation_api_url=TRANSFORMATION_API_URL, parallel_executor=parallel_executor)

  scheduler = Scheduler()
  for config in ADAPTER_CONFIGS:
    adapter = AdapterFactory.create_adapter(adapter_type=config["type"], executor=parallel_executor, **config["kwargs"])
    scheduler.add_job(lambda adapter=adapter: poll_and_transform(adapter, transformer), trigger=config["trigger"], **config["trigger_args"])

  scheduler.start()

  try:
    while True:
      time.sleep(1)
  except (KeyboardInterrupt, SystemExit):
    scheduler.stop()