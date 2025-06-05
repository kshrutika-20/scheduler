from abc import ABC, abstractmethod

class BaseAdapter(ABC):
    def __init__(self, executor):
        self.executor = executor

    @abstractmethod
    def fetch_records(self, query=None):
        pass

    @abstractmethod
    def post_process(self, records, *args, **kwargs):
        pass