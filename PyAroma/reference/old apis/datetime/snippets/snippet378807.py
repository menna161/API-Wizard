import datetime
import logging
import re
import signal
import threading
from timeit import default_timer as timer
import cProfile as profile


def work(self):
    try:
        self.__delay()
        if self.terminate:
            return
        if DEBUG:
            log.debug("Running worker thread '%s'...", self.name)
        self.context['state'] = 'running'
        self.context['first_run'] = datetime.datetime.utcnow().isoformat()
        self.proceed_event.set()
        while (self.__proceed() and (self.loop != 0)):
            if (self.loop > 0):
                self.loop -= 1
            self.target(self, self.context)
            if (self.interval > 0):
                self.context['last_run'] = datetime.datetime.utcnow().isoformat()
                self.wake_event.wait(self.interval)
        self.context['state'] = 'completed'
    except Exception:
        log.exception("Fatal exception in worker thread '%s'", self.name)
        self.context['state'] = 'failed'
        raise
    finally:
        if self.run_on_terminate:
            log.info("Running worker thread '%s' one last time before being terminated", self.name)
            try:
                self.target(self, self.context)
            except:
                log.exception("Failed to run worker thread '%s' one last time before being terminated", self.name)
        log.info("Worker thread '%s' terminated", self.name)
        if (self.registry and self.registry.remove(self)):
            if DEBUG:
                log.debug("Worker thread '%s' removed from registry", self.name)
        else:
            log.warn("Was unable to remove worker thread '%s' from registry", self.name)
