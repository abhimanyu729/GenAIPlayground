from transitions import Machine
import graphviz
from .node_config import NodeState
from .nodes import *

# Shared context for passing data between nodes
class WorkflowContext:
    def __init__(self, lm, documentation):
        self.inputs = None
        self.code = None
        self.fixed_code = None
        self.execution_success = None
        self.errors = None
        self.lm = lm
        self.library_doc = documentation


# The workflow graph using the transitions library
class Workflow:
    states = [
        'collecting_inputs',
        'generating_code',
        'executing_code',
        'fixing_errors',
        'finished',
        'max_retries_reached'
    ]

    def __init__(self, lm, documentation):
        self.context = WorkflowContext(lm, documentation)
        self.nodes = {
            'collecting_inputs': CollectInputsNode('collect_inputs', self.context),
            'generating_code': GenerateCodeNode('generate_code', self.context),
            'executing_code': ExecuteCodeNode('execute_code', self.context),
            'fixing_errors': FixErrorsNode('fix_errors', self.context),
        }
        self.current_node = self.nodes['collecting_inputs']
        self.state = NodeState.COLLECTING_INPUTS
        self.transitions = []  # Track global transitions

        # Set up the state machine
        self.machine = Machine(model=self, states=Workflow.states, initial='collecting_inputs')

        # Define transitions between states
        self.machine.add_transition('collect_inputs', 'collecting_inputs', 'generating_code', conditions='run_collecting_inputs')
        self.machine.add_transition('generate_code', 'generating_code', 'executing_code', conditions='run_generating_code')
        self.machine.add_transition('execute_code', 'executing_code', 'finished', conditions='run_executing_code')
        self.machine.add_transition('execution_failed', 'executing_code', 'fixing_errors')
        self.machine.add_transition('fix_errors', 'fixing_errors', 'executing_code', conditions='run_fixing_errors')
        self.machine.add_transition('max_retries', '*', 'max_retries_reached')

    def run_collecting_inputs(self):
        return self.nodes['collecting_inputs'].run()

    def run_generating_code(self):
        return self.nodes['generating_code'].run()

    def run_executing_code(self):
        success = self.nodes['executing_code'].run()
        if success:
            return True
        else:
            self.execution_failed()
            return False

    def run_fixing_errors(self):
        can_retry = self.nodes['fixing_errors'].run()
        if can_retry:
            return True
        else:
            self.max_retries()
            return False

    def run(self):
        while self.state not in ['finished', 'max_retries_reached']:
            print('Inside Workflow, current state is:', self.state)
            if self.state == 'collecting_inputs':
                self.collect_inputs()
            elif self.state == 'generating_code':
                self.generate_code()
            elif self.state == 'executing_code':
                self.execute_code()
            elif self.state == 'fixing_errors':
                self.fix_errors()

            # Collect global transitions for the workflow graph
            self.transitions.append((self.state, self.current_node.name, self.state))

    def visualize_workflow(self, filename='workflow_graph'):
        dot = graphviz.Digraph(comment='Workflow Execution')
        # Add nodes and edges to the graph
        for node_name, node in self.nodes.items():
            dot.node(node_name, node_name)
            for (source_state, dest_state) in node.transitions:
                dot.edge(source_state.name, dest_state.name, label=f'{node_name}')

        # Render the graph to a file
        dot.render(filename, format='png', cleanup=True)
        print(f"Workflow graph saved as {filename}.png")