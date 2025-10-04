from models.base_model import BaseAIModel
from utils.decorators import timeit, log_call, ensure_input
from utils.mixins import LogMixin, ConfigMixin

class TextClassifier(LogMixin, ConfigMixin, BaseAIModel):
    def __init__(self, model_id="distilbert-base-uncased-finetuned-sst-2-english"):
        super().__init__(model_id, task_name="text-classification")

    @timeit
    @log_call("MODEL")
    @ensure_input((str,))
    def process(self, input_data: str):
        nlp = self.load()
        self.log("Running text classification...")
        
        out = nlp(input_data)
        
        # normalize to a simple dict
        return {"label": out[0]["label"], "score": float(out[0]["score"])}
