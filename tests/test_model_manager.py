from chatbot.core.model_manager import LocalLLM

def test_llm_initialization():
    llm = LocalLLM()
    assert llm is not None

def test_llm_prompt_response(monkeypatch):
    # Dummy-Mock, da echtes Modell groß ist
    class DummyModel:
        def __call__(self, prompt, max_tokens, stop):
            return {"choices": [{"text": "Hello there!"}]}

    llm = LocalLLM()
    llm.model = DummyModel()
    result = llm.ask("Hi!")
    assert "Hello" in result