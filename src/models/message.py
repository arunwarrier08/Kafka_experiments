from dataclasses import dataclass
from datetime import datetime


@dataclass
class Message:
    content: str
    timestamp: datetime = datetime.now()
