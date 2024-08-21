import copy
from enum import Enum, auto

# Define the states for the workflow
class NodeState(Enum):
    COLLECTING_INPUTS = auto()
    GENERATING_CODE = auto()
    EXECUTING_CODE = auto()
    FIXING_ERRORS = auto()
    FINISHED = auto()
    MAX_RETRIES_REACHED = auto()

class NodeConfig:
    def __init__(self):
        # General generation arguments
        self.generation_args_template = {
            "return_full_text": False,
            "do_sample": False,
        }

        self.entity_extraction_generation_args = copy.deepcopy(self.generation_args_template)
        self.code_generation_args = copy.deepcopy(self.generation_args_template)
        self.code_fix_generation_args = copy.deepcopy(self.generation_args_template)

        self.entity_extraction_generation_args.update({"max_new_tokens": 100})
        self.code_generation_args.update({"max_new_tokens": 1000})
        self.code_fix_generation_args.update({"max_new_tokens": 600})

        # Prompts
        self.entity_extraction_prompt_template = [
          {"role": "system", "content": "You are a helpful, and accurate, AI assistant. Always follow the instructions provided by user"},
          {"role": "user", "content": None}, # Placeholder for entity to be extracted
          ]
        self.code_gen_prompt_template = [
            {"role": "system", "content": "You are a helpful, and accurate, AI assistant, that generates bug free executable python code."},
            {"role": "user", "content": "Here is the documentation on how to use the pycaret library for finding best classification model and fit it on new dataset"},
            {"role": "assistant", "content": None},  # Placeholder for library doc
            {"role": "user", "content": None},  # Placeholder for task-specific content
        ]
        self.code_fix_prompt_template = [
            {"role": "system", "content": "You are a helpful, and accurate, AI assistant, that generates bug free executable python code. Follow the output format in the example"},
            {"role": "user", "content": None},  # Placeholder for example error message and code
            {"role": "assistant", "content": None},  # Placeholder for example fixed code
            {"role": "system", "content": "You are a helpful, and accurate, AI assistant, that generates bug free executable python code."},
            {"role": "user", "content": None},  # Placeholder for actual error message and code
        ]

    def get_code_gen_prompt(self, library_doc, task, dataset_url, target_column):
        prompt = copy.deepcopy(self.code_gen_prompt_template)
        prompt[2]["content"] = library_doc
        prompt[3]["content"] = (
            f"Write code to find best model for {task} on dataset located at url: {dataset_url} "
            f"and target column:{target_column} using pycaret library, don't fit it on new data. "
            "Only generate executable code and nothing else like explanation or reasoning"
        )
        return prompt

    def get_code_fix_prompt(self, example_err_msg, example_code_with_error, example_fixed_code, errors, code):
        prompt = copy.deepcopy(self.code_fix_prompt_template)
        prompt[1]["content"] = f"Example: Only generate executable code and nothing else like explanation or reasoning. Fix this error: {example_err_msg} in the python code: {example_code_with_error}."
        prompt[2]["content"] = example_fixed_code
        prompt[4]["content"] = f"Only generate executable code and nothing else like explanation or reasoning. Fix this error: {errors} in the python code: {code}."
        return prompt
