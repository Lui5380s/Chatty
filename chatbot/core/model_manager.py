def generate_response(message: str) -> str:
    """Einfache placeholder-Logik; später ersetzt durch LLM/Retriever."""
    msg = message.lower()
    if "hallo" in msg or "hi" in msg:
        return "Hey 👋! Wie kann ich helfen?"
    if "wer" in msg and "ansprechpartner" in msg:
        return "Der Ansprechpartner ist Max Mustermann."
    if "projekt" in msg:
        return "Dieses Projekt heißt Chatty – dein modularer KI-Assistent für Projekte 🤖"
    if "hilfe" in msg:
        return "Ich kann dir bei Fragen zu deinem Projekt helfen. Frag mich einfach etwas!"
    else:
        return "Sorry, dazu habe ich im Moment keine Daten. Erzähl mir mehr!"