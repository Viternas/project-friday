from enum import Enum
from typing import List, Optional, Dict, Union, Literal, Any
from pydantic import BaseModel, Field, model_validator, field_validator

class ExampleParser(BaseModel):
    outcome: bool = Field(description='The ultimate determination of the review stage')
    reasoning: str = Field(description='The reasoning why this decision was given')

class Complexity(BaseModel):
    score: Literal['LOW', 'MEDIUM', 'HIGH']

    class Config:
        extra = "forbid"

class Checkpoint(BaseModel):
    checkpoint_iter: int = Field(description='The iterative used to track the number of checkpoints')
    description: str = Field(description='The description of the checkpoint activity')
    review_criteria: List[str] = Field(description='The information that is required for the review stage')

class Checkpoints(BaseModel):
    checkpoint: List[Checkpoint]

class SystemQueries(BaseModel):
    question: str
    example_outcomes: List[str]

    class Config:
        extra = 'forbid'

class VerifySystemPrompt(BaseModel):
    clarification_needed_questions: Optional[list[SystemQueries]]

    class Config:
        extra = 'forbid'

class ClarifiedSystemPrompt(BaseModel):
    reformatted_task: str

    class Config:
        extra = 'forbid'




