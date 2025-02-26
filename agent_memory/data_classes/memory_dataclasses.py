from typing import Dict, List, Optional, Set
from dataclasses import dataclass, field

@dataclass
class MemoryParams:
    checkpoint_uuid: str
    step_uuid: str
    previous_step_uuid: str