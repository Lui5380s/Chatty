from llama_cpp import Llama
from pathlib import Path

class LocalLLM:
    def __init__(self, model_path: str | None = None):
        if model_path is None:
            model_path = Path("data/models/llama-3-8b-instruct.Q4_K_M.gguf")

        self.model = Llama(
            model_path=str(model_path),
            n_ctx=2048,
            n_threads=4
        )

    def ask(self, prompt: str) -> str:
        output = self.model(
            f"User: {prompt}\nAssistant:",
            max_tokens=256,
            stop=["User:", "Assistant:"]
        )
        return output["choices"][0]["text"].strip()