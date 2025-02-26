import pprint
from asyncio import current_task
from dataclasses import dataclass
from typing import Dict
from uuid import uuid4

from agent_memory.data_classes.normalizer_dataclasses import FunctionType



def create_example_agent():
    class ExampleAgent:
        def __init__(self, data=None):
            self.agent = data

        def run(self):
            # Implementation here

            pass

        def _map_function(self):
            return {
                'EXAMPLE_FUNCTION': self.example_function,
            }

        @staticmethod
        def _map_arguments():
            return {
                'EXAMPLE_FUNCTION': 'example_function_basemodel',
            }

        def _run_function(self, handler, args_dict, context):
            return handler(**args_dict)

        def single_function_call(self, checkpoint_uuid: str, step_uuid: str, previous_step_uuid: str, function_arguments: dict):
            @self.agent.memory.add_to_memory_decorator()
            @self.agent.memory.function_normalizer.normalize()
            @self.agent.function_type_label(FunctionType.REASONING.value)
            def _single_function_call(*args, **kwargs):
                self.agent.thinking.task = function_arguments.get('checkpoint')
                previous_function = function_arguments.get('previous_function')
                previous_function_output = function_arguments.get('previous_function_output')
                task = function_arguments.get('task')
                single_function_call, cost =\
                    self.agent.thinking.single_function_call(replacement_items=[previous_function, previous_function_output, task])
                return single_function_call, cost
            return  _single_function_call(
                checkpoint_uuid=checkpoint_uuid,
                step_uuid=step_uuid,
                previous_step_uuid=previous_step_uuid,
                function_arguments=function_arguments
            )

        def arguments_for_single_function_call(self, checkpoint_uuid: str, step_uuid: str, previous_step_uuid: str, function_arguments: dict):
            @self.agent.memory.add_to_memory_decorator()
            @self.agent.memory.function_normalizer.normalize()
            @self.agent.function_type_label(FunctionType.REASONING.value)
            def _arguments_for_single_function_call(*args, **kwargs):
                self.agent.thinking.task = function_arguments.get('checkpoint')
                previous_function = function_arguments.get('previous_function')
                previous_function_output = function_arguments.get('previous_function_output')
                task = function_arguments.get('task')
                map_to_args, cost =\
                    self.agent.thinking.arguments_for_single_function_call(replacement_items=[previous_function, previous_function_output, task])
                return map_to_args, cost
            return  _arguments_for_single_function_call(
                checkpoint_uuid=checkpoint_uuid,
                step_uuid=step_uuid,
                previous_step_uuid=previous_step_uuid,
                function_arguments=function_arguments
            )

        def example_function(self, checkpoint_uuid: str, step_uuid: str, previous_step_uuid: str, function_arguments: dict):
            @self.agent.memory.add_to_memory_decorator()
            @self.agent.memory.function_normalizer.normalize()
            @self.agent.function_type_label(FunctionType.REASONING.value)
            def _example_function_processing(*args, **kwargs):
                self.agent.thinking.example_thinking()
                return 5

            @self.agent.memory.add_to_memory_decorator()
            @self.agent.memory.function_normalizer.normalize()
            @self.agent.function_type_label(FunctionType.DATA_PROCESSING.value)
            def _example_function_thinking(*args, **kwargs):
                return 50

            def _run_test_function(*args, **kwargs):
                _example_function_processing(
                    checkpoint_uuid=checkpoint_uuid,
                    step_uuid=step_uuid,
                    previous_step_uuid=previous_step_uuid,
                    function_arguments=function_arguments
                )
                _example_function_thinking(
                    checkpoint_uuid=checkpoint_uuid,
                    step_uuid=str(uuid4()),
                    previous_step_uuid=step_uuid,
                    function_arguments=function_arguments
                )

            return _run_test_function(
                checkpoint_uuid=checkpoint_uuid,
                step_uuid=step_uuid,
                previous_step_uuid=previous_step_uuid,
                function_arguments=function_arguments
            )




    return ExampleAgent()


if __name__ == '__main__':
    run = create_example_agent()
