import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

class LanguageModel:
    def __init__(self, model_name: str = "microsoft/Phi-3-mini-128k-instruct"):
        
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map="auto",
            torch_dtype="auto",
            trust_remote_code=True,
        )
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model.eval()

    def generate_text(self, chat_history: str, generation_args: dict) -> list:
        
        pipe = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
        )

        with torch.no_grad():
          output = pipe(chat_history, **generation_args)
        return output[0]['generated_text'].strip()