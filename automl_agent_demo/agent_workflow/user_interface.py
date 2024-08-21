import pandas as pd
import copy
from .input_validation import DatasetLocationModel

class Conversation:
    def __init__(self, language_model, generation_args, max_retries=5):
        self.lm = language_model
        self.generation_args = generation_args
        self.max_retries = max_retries
        self.dataset_url = None
        self.machine_learning_task = None
        self.target_column = None
        self.supported_ml_tasks = ['classification', 'regression', 'clustering']

    def extract_entities(self, user_input, entity_extraction_prompt_template):
      """Given user input, extract the dataset URL, machine learning task, and target column."""

      # Generate prompt for entity extraction
      dataset_input_prompt = copy.deepcopy(entity_extraction_prompt_template)
      machine_learning_task_input_prompt = copy.deepcopy(entity_extraction_prompt_template)
      target_column_input_prompt = copy.deepcopy(entity_extraction_prompt_template)

      dataset_input_prompt[1]["content"] = f"Given the context: {user_input}. If the context contains a url for a csv or parquet file, return the full url as response, otherwise only ouput one word False"
      machine_learning_task_input_prompt[1]["content"] = f"Given the context: {user_input}. Identify if the context mentions a machine learning task on the target column in the dataset if yes then return the machine learning task as response, like regression or classification or clustering; otherwise only ouput one word False"
      target_column_input_prompt[1]["content"] = f"Given the context: {user_input}. Identify if the context mentions a target column to be used for the machine leraning problem, if yes then return the target column  as response, otherwise only ouput one word False"

      if not self.dataset_url:
        self.dataset_url = self.lm.generate_text(dataset_input_prompt, self.generation_args)
        # Check if the URL is valid
        if not DatasetLocationModel.validate_location(self.dataset_url):
          self.dataset_url = None

      if not self.machine_learning_task:
        self.machine_learning_task = self.lm.generate_text(machine_learning_task_input_prompt, self.generation_args)
        # Check if the machine_learning_task is valid
        if not self.machine_learning_task or self.machine_learning_task.lower() not in self.supported_ml_tasks:
          self.machine_learning_task = None

      if not self.target_column:
        self.target_column = self.lm.generate_text(target_column_input_prompt, self.generation_args)
      # Check if the target_column is valid
      if self.dataset_url:
        data = None
        if self.dataset_url.endswith(".csv"):
          data = pd.read_csv(self.dataset_url, nrows= 10)
        else:
          data = pd.read_parquet(self.dataset_url).head(10)

        if not self.target_column in data.columns:
          self.target_column = None

      return None

    def is_chat_successful(self):
      return self.dataset_url and self.machine_learning_task and self.target_column


    def chat(self, entity_extraction_prompt_template):
      retries = 0
      while retries < self.max_retries and not (self.dataset_url and self.machine_learning_task and self.target_column):
        user_input = input("")
        self.extract_entities(user_input, entity_extraction_prompt_template)
        if self.dataset_url:
          print("Dataset URL:", self.dataset_url)
        else:
          print("Dataset location invalid try again")
        if self.machine_learning_task:
          print("Machine Learning Task:", self.machine_learning_task)
        else:
          print("Please choose machine task from the following: ", self.supported_ml_tasks)
        if self.target_column:
          print("Target:", self.target_column)
        else:
          print("Target columnn not found in the dataset.")

        retries += 1
        if retries == self.max_retries:
          print("Failed to extract entities after multiple retries.")

      return None