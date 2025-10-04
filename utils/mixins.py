class LogMixin:
    def log(self, msg: str):
        print(f"[LOG] {msg}")

class ConfigMixin:
    def set_config(self, **cfg):
        for k, v in cfg.items():
            setattr(self, k, v)
