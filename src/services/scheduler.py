from apscheduler.schedulers.background import BackgroundScheduler
from typing import Callable

class Scheduler:
  def __init__(self):
    self.scheduler = BackgroundScheduler()

  def add_job(self, func: Callable, trigger: str, **kwargs):
    self.scheduler.add_job(func, trigger, **kwargs)

  def start(self):
    self.scheduler.start()

  def stop(self):
    self.scheduler.shutdown()
