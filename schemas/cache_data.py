import datetime
from dataclasses import dataclass
from typing import Optional


@dataclass
class CacheData:
    updated_time: datetime.datetime
    data: Optional[str]
