import os
from uuid import uuid4

from build_utils.encode_config_json import JsonFormatter
from loguru import logger
from openai.resources import Models
from setup_master.master import Master
from build_utils.create_config_class import CreateConfigClass
from utils.ai.ai_enums import *
from api_master import APIMaster
from thinking.thinking import TaskMaster
from agent_registry import map_agent
from agent_memory.agent_internal_memory import AgentMemory


class AgentPrime:
    _memory_initialized = False
    def __init__(self):
        self.ai_driver = None
        self.memory = None

        self.checkpoint_information = None
        self.context = None
        self.work_available = None
        logger.info('Starting AgentPrime')
        self.working_directory = os.path.dirname(__file__)

        self.master = None
        self.CF = None
        self.SE = None
        self.DB = None
        self.AI = None

        self.task_uuid = None
        self.agent_tier = None
        self.agent_uuid = None
        self.work_package_uuid = None

        self.api_master = None
        self.thinking = None

    def initialise_class_runtimes(self):
        logger.info("initializing class runtimes")
        _MASTER_INIT = False
        try:
            self.master = Master(working_dir=self.working_directory, config_file_name='config_main_encoded.json',
                                 config_file_directory=os.path.dirname(__file__))
            _MASTER_INIT = True
        except Exception as e:
            logger.error(f'Error loading class runtimes: {e}')
            return False

        if _MASTER_INIT:
            self.CF = self.master.CF
            self.SE = self.master.SE
            self.DB = self.master.DB
            self.AI = self.master.AI
            logger.info('CF, SE, DB, AI initialised')
            self.api_master = APIMaster(base_port=self.master.SE.base64_decode_string(
                self.master.CF.return_config_orchestration_engine(orchestration_engine_port=True)),
                                        base_url=self.master.SE.base64_decode_string(
                                            self.master.CF.return_config_orchestration_engine(
                                                orchestration_engine_host=True)),
                                        api_key=self.master.SE.base64_decode_string(
                                            self.master.CF.return_config_orchestration_engine(
                                                orchestration_engine_api_key=True)))
            logger.info('Api master initialised')
            self.thinking = TaskMaster(AI_CLIENT=self.AI)
            logger.info('Thinking initialised')
            logger.success("Class runtimes initialised successfully")
            return True

    def initialise_memory_system(self):
        if not AgentPrime._memory_initialized:
            self.memory = AgentMemory(checkpoint=self.checkpoint_information, ai_driver=self.ai_driver)
            self.memory.map_checkpoint_to_dataclass()
            self.memory.build_graph_initial_from_checkpoint_dataclass_list()
            AgentPrime._memory_initialized = True

    def initialise_agent_uuids(self):
        """
        Register with orchestration layer and get task assignments
        """
        logger.info("Initializing agent UUIDs")
        try:
            request = self.api_master.register_heartbeat()
            if request.get('agent_uuid'):
                self.agent_uuid = request.get('agent_uuid')
                logger.info(f'Agent UUID: {self.agent_uuid}')
                self.agent_tier = request.get('agent_tier')
                logger.info(f'Agent Tier: {self.agent_tier}')
                self.task_uuid = request.get('task_uuid')
                logger.info(f'Task UUID: {self.task_uuid}')
                self.work_package_uuid = request.get('work_package_uuid')
                logger.info(f'Work Package UUID: {self.work_package_uuid}')
                self.work_available = True
            else:
                logger.info('No current work available')
                self.work_available = False
            return True
        except Exception as e:
            logger.error(f'Error initializing agent UUIDs: {e}')
            self.work_available = False
            return False

    def get_task_information(self):
        """
        Retrieve detailed task information from the orchestration layer
        """
        logger.info(f"Getting task information for task: {self.task_uuid}")
        try:
            task_info = self.api_master.get_task_information(
                task_uuid=self.task_uuid,
                work_package_uuid=self.work_package_uuid
            )

            if not task_info or not isinstance(task_info, dict):
                logger.error("Failed to retrieve task information")
                return None

            self.context = task_info.get('task_information_obj', {})

            current_context = self.context.get('current_context', {})
            logger.debug(current_context)
            meta_objective = current_context.get('meta_main_objective', {})
            logger.debug(meta_objective)

            logger.debug(f"Task name: {current_context.get('task_name')}")
            logger.debug(f"Task type: {current_context.get('task_type')}")
            logger.debug(f"Task complexity: {current_context.get('task_complexity')}")

            return task_info
        except Exception as e:
            logger.error(f'Error retrieving task information: {e}')
            return None

    def generate_tool_execution_plan(self):
        return

    def check_for_existing_checkpoints(self):
        logger.info(f"Checking checkpoints for task: {self.task_uuid}")
        try:
            checkpoint_info = self.api_master.check_for_checkpoints(
                task_uuid=self.task_uuid,
                work_package_uuid=self.work_package_uuid
            )
            if not checkpoint_info or not isinstance(checkpoint_info, dict):
                logger.error("Failed to retrieve task information")
                return None

            if checkpoint_info.get('checkpoint_information'):
                self.checkpoint_information = checkpoint_info.get('checkpoint_information').get('checkpoint')
                return True
            else:
                return False
        except Exception as e:
            logger.error(f'Error retrieving checkpoint information: {e}')
            return None

    def generate_checkpoints(self):
        logger.info(f"Creating checkpoints for task: {self.task_uuid}")
        try:
            print()
                
        except Exception as e:
            logger.error(f'Error creating checkpoint information: {e}')
            return None

    def initialise_agent_polymorphism(self):
        return

    def run(self):
        if self.initialise_class_runtimes():
            self.initialise_agent_uuids()
            if self.work_available:
                self.get_task_information()
                if not self.check_for_existing_checkpoints():
                    self.generate_checkpoints()
                self.initialise_memory_system()

    def run_example_agent(self):
        test_obj = {
            'checkpoint_uuid': '97e35266-3510-44f2-8d52-bc110da4a0f2',
            'step_uuid': '97e35266-3510-44f2-8d52-bc110da4a0f2',
            'previous_step_uuid': '97e35266-3510-44f2-8d52-bc110da4a0f2',
            'function_arguments': {},
        }

        checkpoint_uuid = list(self.memory.graph_memory.graph.nodes)

        agent_class = map_agent('EXAMPLE')
        handler = agent_class()(self)
        for i in range(5):
            handler.example_function(checkpoint_uuid=checkpoint_uuid[i], step_uuid=str(uuid4()),
                                  previous_step_uuid=checkpoint_uuid[i], function_arguments={})

        self.memory.graph_memory.visualise_plt()

    def test(self):
        self.thinking.task = 'Research the website https://www.project-friday.com, look at everything they have released; I want to know if they have a git hub, funding, team size'
        test, cost = self.thinking.clarify_task(replacement_items=[''])
        print(test)
        exit()
        complexity, cost = self.thinking.evaluate_task_complexity(replacement_items=[self.thinking.task])
        checkpoint, cost = self.thinking.build_web_checkpoint(replacement_items=[complexity.value])
        print(checkpoint)



if __name__ =='__main__':
    #logger.remove()
    run = AgentPrime()
    run.run()
    run.test()

