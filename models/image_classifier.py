from models.base_model import BaseAIModel
from utils.decorators import timeit, log_call, ensure_input
from utils.mixins import LogMixin, ConfigMixin
from PIL import Image

class ImageClassifier(LogMixin, ConfigMixin, BaseAIModel):
    def __init__(self, model_id="google/vit-base-patch16-224"):
        super().__init__(model_id, task_name="image-classification")

    @timeit
    @log_call("MODEL")
    @ensure_input((str,))
    def process(self, input_data: str):
        # input_data is a file path
        pipe = self.load()
        self.log(f"Running image classification on {input_data}...")
        
        img = Image.open(input_data).convert("RGB")
        out = pipe(img)
        
        # take top-3
        return [{"label": x["label"], "score": float(x["score"])} for x in out[:3]]
