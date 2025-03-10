import os
import pathlib
from enum import Enum

base_parent_folder = pathlib.Path(os.path.dirname(__file__)).parent / 'prompts'

class Prompt(Enum):
    EXAMPLE_PROMPT = (f'{base_parent_folder}/example_prompt', ['{replace_var_1}', '{replace_var_2}'])
    WEB_CHECKPOINT_PROMPT = (f'{base_parent_folder}/WEB_CHECKPOINT', ['{task_description}'])
    EVALUATE_TASK_COMPLEXITY = (f'{base_parent_folder}/EVALUATE_TASK_COMPLEXITY', ['{task_description}'])
    CLARIFY_PROMPT = (f'{base_parent_folder}/CLARIFY_PROMPT', ['{}'])
    REWORK_PROMPT = (f'{base_parent_folder}/REWORK_TASK', ['{USER_RESPONSES}'])