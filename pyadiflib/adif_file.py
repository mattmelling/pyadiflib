from typing import Optional, Dict
from datetime import datetime
from dataclasses import dataclass

@dataclass
class AdifFile:
    preamble: Optional[str] = ''
    version: Optional[str] = ''
    created: Optional[datetime] = None
    program_id: Optional[str] = ''
    program_version: Optional[str] = ''
    qsos: Optional[[Dict]] = None
