# --- Base Image ---
FROM condaforge/mambaforge:latest

# --- Arbeitsverzeichnis ---
WORKDIR /app

# --- Pixi installieren ---
RUN curl -fsSL https://pixi.sh/install.sh | bash
ENV PATH="/root/.pixi/bin:$PATH"

# --- Projektdateien kopieren ---
COPY . /app

# --- Pixi Umgebung ---
RUN pixi install

# --- Startbefehl ---
CMD ["pixi", "run", "uvicorn", "chatbot.main:app", "--host", "0.0.0.0", "--port", "8000"]