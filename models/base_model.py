from abc import ABC, abstractmethod
from transformers import pipeline

class BaseAIModel(ABC):
    def __init__(self, model_id: str, task_name: str):
        self._model_id = model_id  # encapsulated detail
        self._task_name = task_name
        self._pipeline = None  # lazy load

    @property
    def model_id(self):
        # controlled access
        return self._model_id

    def load(self):
        """Load pipeline once. Overridable if needed."""
        if self._pipeline is None:
            print(f"Loading model: {self._model_id}...")
            self._pipeline = pipeline(self._task_name, model=self._model_id)
            print("Model loaded.")
        return self._pipeline

    @abstractmethod
    def process(self, input_data):
        """Polymorphic interface: all subclasses must implement."""
        pass
