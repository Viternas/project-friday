from loguru import logger
from thinking.prompt_handler.prompt_handler import PromptHandler
from thinking.enums.prompt_handler_enums import Prompt
from thinking.parsers.parser_basemodels import *
from utils.ai.ai_enums import Models, ClientProvider
from thinking.enums.arb_enums import *


class TaskMaster:
    def __init__(self, AI_CLIENT  = None, task: str = None):
        logger.info(f"Initializing TaskMaster")

        self.ai_client = AI_CLIENT
        self.task = task
        return

    @staticmethod
    def extract_cost_items(usage, model: str) -> dict:
        completion_tokens = usage.completion_tokens  # Gets 2402
        prompt_tokens = usage.prompt_tokens  # Gets 1159
        total_tokens = usage.total_tokens
        model = model

        obj = {'completion_tokens': completion_tokens,
               'prompt_tokens': prompt_tokens,
               'total_tokens': total_tokens,
               'model': model}

        return obj

    def set_prompt(self, PromptEnum, replacement_items):
        prompt = PromptHandler(PromptEnum)
        prompt.get_prompt()
        prompt.build_prompt(replacement_items=replacement_items)
        self.ai_client.agent_prompt = prompt.prompt_content

    def example_function(self, replacement_items, prompt):
        logger.info(f"Running example function")
        cost = []
        self.set_prompt(PromptEnum=Prompt.EXAMPLE_PROMPT, replacement_items=replacement_items)
        print(self.ai_client.agent_prompt)
        self.ai_client.parser = ExampleParser
        self.ai_client.model = Models.GPT_4O.value
        response, cost = self.ai_client.gpt_parse(prompt=prompt)
        cost.append(self.extract_cost_items(usage=cost, model=self.ai_client.model))
        logger.success(f'Example function ran successfully')
        return response, cost

    def clarify_task(self, replacement_items = None):
        logger.info(f'Refining task')
        cost = []
        self.set_prompt(PromptEnum=Prompt.CLARIFY_PROMPT, replacement_items=[''])
        self.ai_client.parser = VerifySystemPrompt
        self.ai_client.model = Models.GPT_4O.model_id
        prompt_clarification, usage = self.ai_client.gpt_parse(prompt=self.task)
        cost.append(self.extract_cost_items(usage=usage, model=self.ai_client.model))
        return prompt_clarification, cost

    def rework_task(self):
        logger.info(f'Reworking task')
        cost = []
        self.ai_client.model = Models.GPT_4O.value
        self.set_prompt(PromptEnum=Prompt.REWORK_PROMPT, replacement_items=[''])
        self.ai_client.parser = ClarifiedSystemPrompt
        prompt_clarification, usage = self.ai_client.gpt_parse(prompt=self.task)
        cost.append(self.extract_cost_items(usage=usage, model=self.ai_client.model))
        return prompt_clarification, cost

    def evaluate_task_complexity(self, replacement_items=''):
        logger.info(f"Evaluating complexity for task: {self.task}")
        cost = []

        self.set_prompt(PromptEnum=Prompt.EVALUATE_TASK_COMPLEXITY, replacement_items=replacement_items)
        self.ai_client.parser = Complexity

        self.ai_client.model = Models.GPT_4O.model_id
        response, usage = self.ai_client.gpt_parse(prompt='')
        cost.append(self.extract_cost_items(usage=usage, model=self.ai_client.model))
        complexity = TaskComplexity(response.score)

        logger.info(f"Task complexity evaluated as: {complexity}")
        return complexity, cost

    def build_web_checkpoint(self, replacement_items):
        usage = []
        logger.info(f"Running web checkpoint creation")
        self.set_prompt(PromptEnum=Prompt.WEB_CHECKPOINT_PROMPT, replacement_items=replacement_items)

        self.ai_client.model = Models.DEEPSEEK_R1.model_id
        steps, cost = self.ai_client.open_router_chat(prompt=str(self.task))
        usage.append(cost)

        self.ai_client.parser = Checkpoints
        self.ai_client.model = Models.GPT_4O.model_id
        steps, cost = self.ai_client.gpt_parse(prompt=steps)
        usage.append(cost)
        return steps, usage


if __name__ == '__main__':
    run = TaskMaster()