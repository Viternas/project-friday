from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Union, List
from datetime import datetime
import uuid
from enum import Enum

class FunctionType(Enum):
    REASONING = "reasoning"
    DATA_PROCESSING = "data_processing"
    PROCESSED_DATA = "processed_data"

@dataclass
class FunctionCost:
    completion_tokens: Optional[int] = None
    prompt_tokens: Optional[int] = None
    total_tokens: Optional[int] = None

@dataclass
class FunctionError:
    type: str
    message: str

@dataclass
class FunctionExecutionOutput:
    function_name: str
    function_signature: str

    function_type: FunctionType
    reasoning: str or None
    data_processing: str or None
    processed_data: str or None

    # Execution metadata
    execution_start: datetime
    execution_end: datetime
    execution_duration: float
    step_uuid: str
    checkpoint_uuid: str
    previous_step_uuid: str

    # Execution details
    status: str  # 'pending', 'success', 'error'
    function_output: Optional[Any] = None
    error: Optional[FunctionError] = None
    cost: Optional[Union[Dict, List[Dict]]] = None

    # Output characteristics
    function_output_type: Optional[str] = None
    has_iter: bool = False
    is_empty: bool = True
    has_markdown: bool = False
    iteration_count: Optional[int] = None

    # Arguments provided
    args_provided: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass to a dictionary format."""
        return {
            'function_name': self.function_name,
            'function_signature': self.function_signature,
            'execution_start': self.execution_start.isoformat(),
            'execution_end': self.execution_end.isoformat(),
            'execution_duration': self.execution_duration,
            'step_uuid': self.step_uuid,
            'checkpoint_uuid': self.checkpoint_uuid,
            'status': self.status,
            'function_output': self.function_output,
            'error': vars(self.error) if self.error else None,
            'cost': vars(self.cost) if self.cost else None,
            'function_output_type': self.function_output_type,
            'has_iter': self.has_iter,
            'is_empty': self.is_empty,
            'has_markdown': self.has_markdown,
            'iteration_count': self.iteration_count,
            'args_provided': self.args_provided
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FunctionExecutionOutput':
        """Create a FunctionExecutionOutput instance from a dictionary."""
        # Convert string timestamps back to datetime
        data['execution_start'] = datetime.fromisoformat(data['execution_start'])
        data['execution_end'] = datetime.fromisoformat(data['execution_end'])

        # Convert error dict to FunctionError if present
        if data.get('error'):
            data['error'] = FunctionError(**data['error'])

        # Convert cost dict to FunctionCost if present
        if data.get('cost'):
            data['cost'] = FunctionCost(**data['cost'])

        return cls(**data)

    def to_embedding_text(self) -> str:
        """Generate a rich text representation for embedding."""
        error_text = f"Error: {self.error.type} - {self.error.message}" if self.error else "No errors"
        cost_text = f"Tokens used: {self.cost.total_tokens}" if self.cost else "No cost data"

        return f"""
                        Function execution: {self.function_name}{self.function_signature}
                        Status: {self.status}
                        Execution time: {self.execution_duration:.6f} seconds
                        Output type: {self.function_output_type}
                        Output: {str(self.function_output)}
                        {error_text}
                        {cost_text}
                        Iteration count: {self.iteration_count if self.iteration_count is not None else 'N/A'}
                        Additional characteristics: {'Iterable' if self.has_iter else 'Non-iterable'}, 
                        {'Empty' if self.is_empty else 'Non-empty'}, 
                        {'Contains Markdown' if self.has_markdown else 'No Markdown'}
                        Execution IDs: Step {self.step_uuid}, Checkpoint {self.checkpoint_uuid}
                        """.strip()