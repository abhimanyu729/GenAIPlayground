This repository contains code for a AutoML LLM Agent Demo. The project demonstrates a proof of concept system that can automatically generate code for finding best machine learning model for a given user problem using large language models (LLMs). The system integrates multiple components to extract documentation and entities, generate, execute, and debug code automatically. This is achieved through a state machine workflow, with each step being managed by specific nodes that interact with an LLM.

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Customization](#customization)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

This project leverages the power of LLMs to automate the following tasks:
- Extract relevant entities from user input, such as dataset URLs, machine learning tasks, and target columns.
- Generate Python code for machine learning tasks based on user-provided documentation and dataset.
- Execute the generated code and handle any errors that arise.
- Automatically fix errors in the code and re-execute it until successful completion or until a maximum number of retries is reached.

## Features

- **Language Model Integration**: Utilizes pre-trained models from the Hugging Face Transformers library for text generation.
- **Entity Extraction**: Identifies key entities (e.g., dataset URLs, ML tasks) from user input using an LLM.
- **Code Generation**: Automatically generates Python code for machine learning tasks using AutoML libraries based on extracted entities and provided documentation.
- **Error Handling**: Executes the generated code, captures errors, and uses the LLM to automatically fix and re-run the code.
- **State Machine Workflow**: Implements a state machine to manage the workflow, including transitions between states such as input collection, code generation, code execution, and error fixing.
- **Visualization**: Generates a visual representation of the workflow execution using Graphviz.

## Requirements

- Python 3.8+
- [Torch](https://pytorch.org/) (tested with version 1.11+)
- [Transformers](https://huggingface.co/docs/transformers/index) (tested with version 4.0+)
- [Pydantic](https://pydantic-docs.helpmanual.io/) (tested with version 1.10+)
- [Requests](https://docs.python-requests.org/en/master/)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Graphviz](https://graphviz.org/)
- [Transitions](https://github.com/pytransitions/transitions)

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/abhimanyu729/GenAIPlayground.git
    cd your-repo-name
    ```

2. **Create a virtual environment** (optional but recommended):
    ```bash
    python3 -m venv venv
    source venv/bin/activate 
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Download a pre-trained model**:
    Update the `model_name` in the script to the desired pre-trained model from Hugging Face. The default is `microsoft/Phi-3-mini-128k-instruct`.

2. **Run the workflow**:
    ```bash
    python your_script.py
    ```
    Follow the prompts to input the dataset URL, machine learning task, and target column.

3. **Visualize the workflow**:
    After running the script, a PNG file of the workflow execution will be generated. This visual representation shows the state transitions and flow of the entire process.

## Project Structure

```
├── README.md                # Project documentation
├── your_script.py           # Main script for running the workflow
├── requirements.txt         # List of dependencies
└── workflow_modules/        # Directory containing the modules
    ├── language_model.py    # Module for handling the language model
    ├── workflow.py          # Module for managing the workflow and states
    ├── nodes.py             # Module containing the various node classes
    ├── utils.py             # Utility functions
    └── visualization.py     # Module for workflow visualization
```

## Customization

- **Adding New Nodes**: To add new nodes, define a new class in `nodes.py` and integrate it into the workflow state machine in `workflow.py`.
- **Model Customization**: You can replace the default language model by changing the `model_name` in the `LanguageModel` class. Ensure that the new model supports the required tasks.
- **Generation Arguments**: Modify the generation arguments in the `NodeConfig` class to fine-tune the behavior of the text generation.

## Contributing

We welcome contributions to improve this project! Please fork the repository and submit a pull request with your changes. Ensure that your code adheres to PEP 8 standards and is well-documented.

## License

This project is licensed under the Apache License. See the [LICENSE](LICENSE) file for details.