from typing import Dict, List, Optional, Set
from dataclasses import dataclass, field


@dataclass
class CheckPoints:
    checkpoint_uuid: str
    checkpoint_iterator: int
    checkpoint_description: str
    checkpoint_review_criteria: list[str]

@dataclass
class FunctionName:
    a: str

@dataclass
class FunctionArguments:
    a: str

@dataclass
class FunctionOutputs:
    a: str

