from loguru import logger
from thinking.prompt_handler.prompt_handler import PromptHandler
from thinking.enums.prompt_handler_enums import Prompt
from thinking.parsers.parser_basemodels import *
from utils.ai.ai_enums import Models, ClientProvider


class TaskMaster:
    def __init__(self, AI_CLIENT  = None):
        logger.info(f"Initializing TaskMaster")

        self.ai_client = AI_CLIENT
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
        self.ai_client.parser = ExampleParser
        self.ai_client.model = Models.GPT_4O.value
        response, cost = self.ai_client.gpt_parse(prompt=prompt)
        cost.append(self.extract_cost_items(usage=cost, model=self.ai_client.model))
        logger.success(f'Example function ran successfully')
        return response, cost


if __name__ == '__main__':
    run = TaskMaster()