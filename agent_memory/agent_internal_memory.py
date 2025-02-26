from functools import wraps
from typing import Callable, Any
from uuid import uuid4

from loguru import logger

from agent_memory.graph_tooling.graph_dag import GraphDag
from agent_memory.function_normalizer.function_normalizer import FunctionOutputNormalizer
from agent_memory.data_classes.normalizer_dataclasses import *
from agent_memory.data_classes.memory_dataclasses import *
from agent_memory.data_classes.graph_dataclasses import *
from agent_memory.graph_tooling.state_management import StateManagement
from agent_memory.hash_rag.HashRag import HashRag



class AgentMemory:
    def __init__(self, ai_driver, checkpoint: list[CheckPoints] = None, work_package_uuid: str = None, task_uuid: str = None,
                 checkpoint_uuid: str = None):
        logger.info("Initializing AgentMemory")
        self.ai_driver = ai_driver
        self.checkpoint_uuid = checkpoint_uuid
        self.task_uuid = task_uuid
        self.work_package_uuid = work_package_uuid
        self.graph_memory = GraphDag()
        self.function_normalizer = FunctionOutputNormalizer()
        self.state_management = StateManagement(MemoryClass=self.graph_memory)
        self.hash_rag = HashRag(ai_driver=self.ai_driver)
        self.checkpoint = checkpoint
        self.checkpoint_dataclass_list = []
        logger.debug(f"AgentMemory initialized with work_package_uuid: {work_package_uuid}, task_uuid: {task_uuid}")
        return

    @staticmethod
    def function_type_label(label: FunctionType):
        """
        A simple decorator that attaches a 'function_label' attribute
        to the decorated function.
        """

        def decorator(func):
            func.function_type_label = label  # Attach the label as an attribute
            return func

        return decorator

    def map_checkpoint_to_dataclass(self):
        logger.info("Mapping checkpoints to dataclass")
        try:
            for checkpoint in self.checkpoint:

                checkpoint_uuid = str(uuid4())
                logger.debug(f"Creating checkpoint with UUID: {checkpoint_uuid}")
                self.checkpoint_dataclass_list.append(CheckPoints(
                    checkpoint_uuid=checkpoint_uuid,
                    checkpoint_iterator=checkpoint.get('checkpoint_iter'),
                    checkpoint_description=checkpoint.get('description'),
                    checkpoint_review_criteria=checkpoint.get('review_criteria')
                ))
            logger.success(f"Successfully mapped {len(self.checkpoint_dataclass_list)} checkpoints")
        except Exception as e:
            logger.error(f"Error mapping checkpoints to dataclass: {str(e)}")
            raise
        return

    def build_graph_initial_from_checkpoint_dataclass_list(self):
        logger.info("Building initial graph from checkpoint dataclass list")
        if self.checkpoint_dataclass_list:
            try:
                self.graph_memory.checkpoints = self.checkpoint_dataclass_list
                self.graph_memory.build_checkpoints()
                logger.success("Successfully built graph from checkpoints")
            except Exception as e:
                logger.error(f"Error building graph: {str(e)}")
                raise
        else:
            logger.error("No checkpoint dataclass list available")
            raise ValueError("Checkpoint dataclass list is empty")

    def run_function(self, function_handler):
        logger.info(f"Running function: {function_handler.__name__}")
        try:
            function_output = self.function_normalizer.normalize(function_handler)
            self.add_function_to_memory(function_output=function_output)
            logger.success(f"Successfully executed function: {function_handler.__name__}")
            return function_output
        except Exception as e:
            logger.error(f"Error running function {function_handler.__name__}: {str(e)}")
            raise

    def add_function_to_memory(self, function_output):
        logger.info("Adding function output to memory")
        try:
            self.hash_rag.data_for_rag = function_output
            #self.hash_rag.tester()
            logger.success("Successfully added function output to memory")
        except Exception as e:
            logger.error(f"Error adding function to memory: {str(e)}")
            raise
        return

    def add_steps_to_memory(self, normalised_output, checkpoint_uuid, step_uuid):
        logger.info(f"Adding steps to memory - Step UUID: {step_uuid}, Checkpoint UUID: {checkpoint_uuid}")
        try:
            normalised_output.step_uuid = step_uuid
            normalised_output.checkpoint_uuid = checkpoint_uuid
            self._add_to_graph(step_object=normalised_output)
            self.add_function_to_memory(function_output=normalised_output)
            logger.success("Successfully added steps to memory")
        except Exception as e:
            logger.error(f"Error adding steps to memory: {str(e)}")
            raise
        return

    def _add_to_graph(self, step_object):
        logger.debug(f"Adding step object to graph - UUID: {step_object.step_uuid}")
        try:
            self.graph_memory.add_execution_steps(step_object)
            logger.success("Successfully added step to graph")
        except Exception as e:
            logger.error(f"Error adding step to graph: {str(e)}")
            raise

    def _add_to_rag(self, step_object):
        logger.debug("Adding to RAG")
        return

    def get_checkpoint(self):
        logger.info("Getting checkpoint")
        try:
            checkpoint = self.state_management.get_checkpoint()
            logger.success("Successfully retrieved checkpoint")
            return checkpoint
        except Exception as e:
            logger.error(f"Error getting checkpoint: {str(e)}")
            raise

    def add_to_memory_decorator(self):
        """
        Decorator to add function output to AgentMemory.
        Now properly handles the order of operations for normalization.
        """

        def decorator(handler: Callable) -> Callable:
            @wraps(handler)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                checkpoint_uuid = kwargs.get('checkpoint_uuid')
                step_uuid = kwargs.get('step_uuid')

                output = handler(*args, **kwargs)

                if isinstance(output, FunctionExecutionOutput):
                    if checkpoint_uuid:
                        output.checkpoint_uuid = checkpoint_uuid
                    if step_uuid:
                        output.step_uuid = step_uuid

                    self.add_steps_to_memory(normalised_output=output, checkpoint_uuid=checkpoint_uuid, step_uuid=step_uuid)

                return output

            return wrapper

        return decorator


if __name__ == '__main__':
    logger.info("Starting main execution")
    try:
        run = AgentMemory()
        run._map_checkpoint_to_dataclass()
        run.build_graph_initial_from_checkpoint_dataclass_list()
        logger.success("Main execution completed successfully")
    except Exception as e:
        logger.critical(f"Critical error in main execution: {str(e)}")
        raise