from pathlib import Path
from typing import Optional, List
from loguru import logger
from thinking.enums.prompt_handler_enums import Prompt


class PromptHandler:
    def __init__(self, prompt: Prompt):

        self.prompt = prompt
        self.prompt_path = Path(self.prompt.value[0])
        self.replacement_values = self.prompt.value[1]
        self.prompt_content: Optional[str] = None

        logger.debug(f"Initialized PromptHandler with prompt: {self.prompt}")

    def load_prompt(self) -> Optional[str]:

        logger.info(f"Attempting to load prompt from {self.prompt_path}")

        if not self.prompt_path.exists():
            logger.error(f"Prompt file does not exist: {self.prompt_path}")
            return None

        try:
            self.prompt_content = self.prompt_path.read_text(encoding='utf-8')
            logger.info(f"Successfully loaded prompt from {self.prompt_path}")
            return self.prompt_content
        except IOError as e:
            logger.error(f"IOError while reading the prompt file: {e}")
        except Exception as e:
            logger.error(f"Unexpected error while loading prompt: {e}")

        return None

    def get_prompt(self) -> Optional[str]:

        if self.prompt_content is None:
            return self.load_prompt()
        return self.prompt_content

    def build_prompt(self, replacement_items: List[str]):
        if len(self.replacement_values) != len(replacement_items):
            raise ValueError(
                f"Number of replacements ({len(replacement_items)}) does not match number of placeholders ({len(self.replacement_values)}).")

        for placeholder, replacement in zip(self.replacement_values, replacement_items):
            self.prompt_content = self.prompt_content.replace(placeholder, str(replacement))



if __name__ == "__main__":
    print()
