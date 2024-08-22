from agent_workflow.language_model import LanguageModel
from agent_workflow.workflow import Workflow
from agent_workflow.utils import DataExtractor

def main():

    documentation_url = input("Enter URL of an AutoML library's documentation: ")
    raw_html = DataExtractor().fetch_url_content(documentation_url)
    documentation_context = None
    if raw_html:
        documentation_context = DataExtractor().extract_data(raw_html)

    model_name = "microsoft/Phi-3-mini-128k-instruct"
    lm = LanguageModel(model_name)
    workflow = Workflow(lm, documentation_context)
    workflow.run()
    workflow.visualize_workflow(filename='workflow_graph_execution')

if __name__ == "__main__":
    main()
