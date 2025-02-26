import os
import pathlib
from enum import Enum

base_parent_folder = pathlib.Path(os.path.dirname(__file__)).parent / 'prompts'

class Prompt(Enum):
    EXAMPLE_PROMPT = (f'{base_parent_folder}/example_prompt', '{replace_var_1}', '{replace_var_2}')