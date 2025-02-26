from typing import Callable, Any, Dict, Optional, Tuple, Union, List
from datetime import datetime
import inspect
from functools import wraps
from agent_memory.data_classes.normalizer_dataclasses import *
from loguru import logger

class FunctionOutputNormalizer:
    """
    Normalizes the output of functions, capturing execution details, and providing
    structured information about the function's execution and results.
    """

    @staticmethod
    def _get_iteration_count(output: Any) -> Optional[int]:
        """
        Gets the iteration count by examining containers for content length.  Handles
        more cases and provides more robust iteration counting.  Uses `isinstance`
        checks *before* attempting attribute access for improved safety.
        """
        if isinstance(output, (list, tuple, set, dict)):
            return len(output)
        elif isinstance(output, str) or isinstance(output, bytes):
            return None
        elif hasattr(output, '__len__'):
            try:
                return len(output)
            except TypeError:
                return None
        elif hasattr(output, '__iter__'):
            try:
                return sum(1 for _ in output)
            except TypeError:
                return None
        return None

    @staticmethod
    def _is_cost_data(item: Any) -> bool:
        """
        Determines if an item represents cost data.  Uses a set for faster key lookups.
        Handles nested structures more robustly.
        """
        cost_keys = {'completion_tokens', 'prompt_tokens', 'total_tokens'}
        if isinstance(item, dict):
            return any(key in cost_keys for key in item)  # Faster set lookup
        elif isinstance(item, list):
            return any(FunctionOutputNormalizer._is_cost_data(element) for element in item)
        return False

    @staticmethod
    def _extract_cost(output: Any) -> Tuple[Any, Optional[Any]]:
        """
        Extracts cost information from function output.  Handles various output types
        (including non-iterable) and uses recursion for nested structures.
        """
        if not isinstance(output, (list, tuple)):
            return output, None

        output_list = list(output)
        cost_data = None
        indices_to_remove = []

        for i, item in enumerate(output_list):
            if FunctionOutputNormalizer._is_cost_data(item):
                cost_data = item
                indices_to_remove.append(i)
                break

        for idx in reversed(indices_to_remove):
            del output_list[idx]

        if not output_list:
            output_only = None
        elif len(output_list) == 1:
            output_only = output_list[0]
        else:
            output_only = tuple(output_list) if isinstance(output, tuple) else output_list

        return output_only, cost_data

    @staticmethod
    def _is_markdown(output: Any) -> bool:
        """
        Checks if the output is likely Markdown formatted.  Uses a set for faster lookups.
        """
        markdown_keys = {'links', 'extracted_content'}
        return isinstance(output, dict) and any(key in markdown_keys for key in output)

    @classmethod
    def _normalise_function_output(cls, handler: Callable, *args, **kwargs) -> Dict[str, Any]:
        """
        Normalizes function output (internal method).  This is the lower-level
        normalization, returning a dictionary.
        """
        start_time = datetime.now()
        return_obj = {
            'function_name': handler.__name__,
            'function_signature': str(inspect.signature(handler)),
            'execution_start': start_time.isoformat(),
            'args_provided': {
                'args': args,
                'kwargs': kwargs
            },
            'status': 'pending',
            'error': None,
        }

        try:
            raw_output = handler(*args, **kwargs)
            output, cost = cls._extract_cost(raw_output)

            return_obj.update({
                'status': 'success',
                'function_output': output,
                'cost': cost,
                'function_output_type': type(output).__name__ if output is not None else 'NoneType',
                'has_iter': hasattr(output, '__iter__') and not isinstance(output, (str, bytes)),
                'is_empty': output is None or (isinstance(output, (list, tuple, dict, str)) and len(output) == 0),
                'has_markdown': cls._is_markdown(output),
            })

            iteration_count = cls._get_iteration_count(output)
            if iteration_count is not None:
                return_obj['iteration_count'] = iteration_count

        except Exception as e:
            logger.exception("Error during function execution: %s", e)
            return_obj.update({
                'status': 'error',
                'error': {
                    'type': type(e).__name__,
                    'message': str(e)
                },
                'function_output': None
            })

        finally:
            end_time = datetime.now()
            return_obj.update({
                'execution_end': end_time.isoformat(),
                'execution_duration': (end_time - start_time).total_seconds()
            })

        return return_obj

    @classmethod
    def normalize(cls, handler=None):
        """
        Decorator that normalizes function output. Can be used with or without parameters.

        Args:
            handler: The function to be decorated (when used without parameters)
            step_uuid: Optional step UUID for tracking
            checkpoint_uuid: Optional checkpoint UUID for tracking
        """

        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args: Any, **kwargs: Any) -> FunctionExecutionOutput:
                start_time = datetime.now()
                output: Any = None
                cost_data: Optional[FunctionCost] = None
                error: Optional[FunctionError] = None
                status: str = 'pending'
                step_uuid = kwargs.pop('step_uuid', '')
                checkpoint_uuid = kwargs.pop('checkpoint_uuid', '')
                previous_step_uuid = kwargs.pop('previous_step_uuid', '')

                try:
                    raw_output = func(*args, **kwargs)
                    print(raw_output)
                    output, cost = cls._extract_cost(raw_output)

                    if hasattr(func, 'function_type_label'):
                        function_label = func.function_type_label

                    if cost:
                        cost = cost
                    else:
                        cost = None
                    status = 'success'

                except Exception as e:
                    logger.exception(f"Error during function execution: {e}")
                    status = 'error'
                    error = FunctionError(type=type(e).__name__, message=str(e))

                finally:
                    end_time = datetime.now()
                    execution_duration = (end_time - start_time).total_seconds()

                try:
                    function_execution_output = FunctionExecutionOutput(
                        step_uuid=step_uuid,
                        checkpoint_uuid=checkpoint_uuid,
                        previous_step_uuid=previous_step_uuid,
                        function_type=function_label,
                        reasoning=None,
                        data_processing=None,
                        processed_data=None,
                        function_name=func.__name__,
                        function_signature=str(inspect.signature(func)),
                        execution_start=start_time,
                        execution_end=end_time,
                        execution_duration=execution_duration,
                        status=status,
                        function_output=output,
                        error=error,
                        cost=cost_data,
                        function_output_type=type(output).__name__ if output is not None else 'NoneType',
                        has_iter=hasattr(output, '__iter__') and not isinstance(output, (str, bytes)),
                        is_empty=output is None or (isinstance(output, (list, tuple, dict, str)) and len(output) == 0),
                        has_markdown=cls._is_markdown(output),
                        iteration_count=cls._get_iteration_count(output),
                        args_provided={'args': args, 'kwargs': kwargs}
                    )
                    def _get_reasoning():
                        function_execution_output.reasoning = output.action_type_reason

                    def _get_data_processing():
                        function_execution_output.data_processing = 'data_processing'

                    def _get_processed_data():
                        function_execution_output.processed_data = 'processed_data'

                    function_type_mapper = {
                     "reasoning": _get_reasoning,
                    "data_processing": _get_data_processing,
                    "processed_data": _get_processed_data,
                    }
                    if function_label in function_type_mapper:
                        function_type_mapper[function_label]()

                    return function_execution_output
                except Exception as e:
                    logger.exception(f"Error creating FunctionExecutionOutput: {e}")
                    return cls._normalise_function_output(func, *args, **kwargs)

            return wrapper

        if handler is None:
            return decorator
        return decorator(handler)


