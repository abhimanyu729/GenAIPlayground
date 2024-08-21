import traceback
from .node_config import NodeConfig
from .conversation import Conversation

# Base class for all nodes in the workflow
class Node:
    def __init__(self, name, context, retries= 5):
        self.name = name
        self.context = context
        self.max_retries = retries
        self.transitions = []  # Track transitions for visualization

    def run(self):
        raise NotImplementedError("Each node must implement the run method")

    def log_transition(self, source_state, dest_state):
      self.transitions.append((source_state, dest_state))

# Node for collecting inputs
class CollectInputsNode(Node):
    def run(self):
        # Logic to collect inputs
        source_state = NodeState.COLLECTING_INPUTS
        self.context.inputs = self.collect_inputs()
        if self.inputs_collected():
            dest_state = NodeState.GENERATING_CODE
            self.log_transition(source_state, dest_state)
            return True
        else:
          dest_state = NodeState.COLLECTING_INPUTS
          self.log_transition(source_state, dest_state)
          return False

    def collect_inputs(self):
        # Define generation arguments
        config = NodeConfig()
        # Initialize Conversation
        conversor = Conversation(self.context.lm, config.entity_extraction_generation_args, self.max_retries)
        conversor.chat(config.entity_extraction_prompt_template)
        if conversor.is_chat_successful():
          return {'dataset_url': conversor.dataset_url, 'machine_learning_task': conversor.machine_learning_task, 'target_column': conversor.target_column}
        return None


    def inputs_collected(self):
        # Implement logic to check if inputs are collected
        return self.context.inputs is not None

# Node for generating code
class GenerateCodeNode(Node):
    def run(self):
        # Logic to generate code

        config = NodeConfig()
        prompt = config.get_code_gen_prompt(
            self.context.library_doc,
            self.context.inputs['machine_learning_task'],
            self.context.inputs['dataset_url'],
            self.context.inputs['target_column']
        )
        self.context.code = self.generate_code(prompt, config.code_generation_args)
        # self.context.code = " " + self.context.code
        source_state = NodeState.GENERATING_CODE
        dest_state = NodeState.EXECUTING_CODE
        self.log_transition(source_state, dest_state)
        return True

    def generate_code(self, code_gen_prompt, code_generation_args):
        # Implement code generation logic
        return self.context.lm.generate_text(code_gen_prompt, code_generation_args)

# Node for executing code
class ExecuteCodeNode(Node):
    def run(self):
        # Logic to execute code
        source_state = NodeState.EXECUTING_CODE
        success, errors = self.execute_code(self.context.code)
        self.context.execution_success = success
        self.context.errors = errors
        if success:
            dest_state = NodeState.FINISHED
        else:
            dest_state = NodeState.FIXING_ERRORS
        self.log_transition(source_state, dest_state)

        return success

    def execute_code(self, code):
        # code execution logic
        try:
            print(code)
            exec(code)
            return True, None  # Indicate successful execution
        except Exception as e:
            error_message = str(traceback.format_exc())
            return False, [error_message]

# Node for fixing errors
class FixErrorsNode(Node):
    def __init__(self, name, context, max_retries=3):
        super().__init__(name, context)
        self.retries = 0
        self.max_retries = max_retries

    def run(self):
        # Logic to fix errors
        source_state = NodeState.FIXING_ERRORS
        self.context.fixed_code = self.fix_errors(self.context.errors, self.context.code)
        self.context.code = self.context.fixed_code
        self.retries += 1
        if self.retries >= self.max_retries:
            dest_state = NodeState.MAX_RETRIES_REACHED
        else:
            dest_state = NodeState.EXECUTING_CODE
        self.log_transition(source_state, dest_state)
        return self.retries < self.max_retries

    def fix_errors(self, errors, code):
        # Implement error fixing logic
        example_err_msg = (
            "Traceback (most recent call last):\n"
            '  File "<ipython-input-48-a50281d5d318>", line 3, in <cell line: 2>\n'
            "    exec(code_2_run)\n"
            '  File "<string>", line 6, in <module>\n'
            "NameError: name 'adde_two_numbers' is not defined"
        )

        example_code_with_error = (
            "def add_two_numbers(a, b):\n"
            "    return a + b\n\n"
            "a = 10\n"
            "b = 5\n"
            "print(adde_two_numbers(a, b))"
        )

        example_fixed_code = (
            "# Here is the fixed code\n"
            "def add_two_numbers(a, b):\n"
            "    return a + b\n\n"
            "a = 10\n"
            "b = 5\n"
            "print(add_two_numbers(a, b))"
        )
        prompt = NodeConfig().get_code_fix_prompt(
            example_err_msg,
            example_code_with_error,
            example_fixed_code,
            errors,
            code
        )
        return self.context.lm.generate_text(prompt, NodeConfig().code_fix_generation_args)