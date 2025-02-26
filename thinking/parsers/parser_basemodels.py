from enum import Enum
from typing import List, Optional, Dict, Union, Literal, Any
from pydantic import BaseModel, Field, model_validator, field_validator

class ExampleParser(BaseModel):
    outcome: bool = Field(description='The ultimate determination of the review stage')
    reasoning: str = Field(description='The reasoning why this decision was given')



