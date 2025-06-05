from apscheduler.schedulers.background import BackgroundScheduler
from src.factories.adapter_factory import AdapterFactory
from typing import List
import logging

logger = logging.getLogger(__name__)

class SchedulerService:
    def __init__(self, transformer, executor):
        self.scheduler = BackgroundScheduler()
        self.transformer = transformer
        self.executor = executor

    def load_jobs(self, adapter_configs: List[dict]):
        for adapter_config in adapter_configs:
            adapter = AdapterFactory.create(adapter_config['type'], self.executor, **adapter_config['kwargs'])
            self.scheduler.add_job(
                lambda adapter_instance=adapter, config=adapter_config: self._execute(adapter_instance, config),
                trigger=adapter_config['trigger'],
                **adapter_config['trigger_args']
            )

    def _execute(self, adapter_instance, adapter_config):
        query = adapter_config['kwargs'].get('query_template')
        mutation = adapter_config['kwargs'].get('mutation_template')

        records = adapter_instance.fetch_records(query)
        if not records:
            logger.info("No records to process")
            return

        if adapter_config['type'] == 'mongo':
            results = self.transformer.transform_records(records)
            successful = [record for record, success in zip(records, results) if success]
            failed = [record for record, success in zip(records, results) if not success]

            if successful:
                adapter_instance.post_process(successful)

            if failed:
                logger.warning(f"{len(failed)} records failed transformation.")
                if hasattr(adapter_instance, "mark_failed"):
                    adapter_instance.mark_failed(failed)
        else:
            adapter_instance.post_process(records, mutation)

    def start(self):
        self.scheduler.start()

    def stop(self):
        self.scheduler.shutdown()