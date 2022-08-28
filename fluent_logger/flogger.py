from fluent import sender
from dataclasses import dataclass, asdict
from ujson import dumps, loads

FLUENT_SERVER_IP = "100.92.192.3"
logger = sender.FluentSender('project', host=FLUENT_SERVER_IP, port=24224)


@dataclass()
class FLogger:
    tag = "log"

    def dict(self):
        return asdict(self)

    def log(self):
        logger.emit(self.tag, self.dict())

    def error(self):
        logger.emit(f"{self.tag}.error", self.dict())
