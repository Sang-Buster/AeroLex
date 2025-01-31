<div align="center">
   <a href="https://github.com/Sang-Buster/AeroLex">
      <img src="/READ.assets/favicon.ico" width=30% alt="logo">
   </a>   
   <h1>AeroLex - Making Airwaves Understandable</h1>
   <h6><small>An AI-powered ATC Communication Analysis Tool</small></h6>
   <p><b>#LLM &emsp; #Air Traffic Control Communication &emsp; #Automatic Speech Recognition <br/>#Name Entity Recognition</b></p>
</div>

---

<div align="center">
  <h2>🔍 Table of Contents</h2>
</div>

- [✨ Features](#-key-features)
- [👨‍💻 Tech Stack](#-tech-stack)
- [🚀 Getting Started](#-getting-started)
- [⚒️ Development Setup](#-development-setup)
- [📝 File Structure](#-file-structure)
- [🤝 Contributing](#-contributing)

---

<div align="center">
  <h2>✨ Key Features</h2>
</div>

AeroLex is an AI-powered web application that transcribes, visualizes, and analyzes air traffic communication. Using advanced speech recognition (Whisper), named entity recognition (SpaCy), and language models (Ollama), it transforms ATC conversations into structured, actionable insights. Some of the key features are:
  - **Audio Processing**
    - Upload and record audio files
    - Visualize audio distribution (waveform, spectrogram, etc.)
  - **Speech Recognition & Transcription**
    - Live transcription using Whisper or other ASR models
    - Support for air traffic control (ATC) communication
  - **Text Processing & Annotation**
    - Upload text files or input manually
    - Named Entity Recognition (NER) for aviation terms (call signs, waypoints, altitudes, etc.)
    - Text annotation with XML-like tagging
  - **Data Analysis & Insights**
    - Tokenization, keyword extraction, and entity recognition
    - Report generation using LLMs (Ollama)
  - **Web App with Streamlit**
    - Sidebar navigation with multiple functional pages
    - Interactive visualizations and text processing tools

---

<div align="center">
  <h2>👨‍💻 Tech Stack</h2>
</div>

- ffmpeg (for audio processing)
- Whisper ASR (OpenAI)
- Ollama (for LLMs)
- Mapbox (for map visualization)
- SpaCy (for NER)
- Streamlit (for UI)

---

<div align="center">
  <h2>🚀 Getting Started</h2>
</div>

1. **Clone the repository and navigate to project folder:**
   ```bash
   git clone https://github.com/Sang-Buster/AeroLex
   cd AeroLex
   ```

2. **Install [uv](https://docs.astral.sh/uv/) first:**
   ```bash
   # macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

   ```bash
   # Windows
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

3. **Create a virtual environment at `AeroLex/.venv/`:**
   ```bash
   uv venv --python 3.12.1
   ```

4. **Activate the virtual environment:**
   ```bash
   # macOS/Linux
   source .venv/bin/activate
   ```

   ```bash
   # Windows
   .venv\Scripts\activate
   ```

5. **Install the required packages:**
   ```bash
   uv pip install -r requirements.txt
   ```

<div align="center">
  <h2>⚒️ Development Setup</h2>
</div>

1. **Set up environment variables:**
   ```bash
   # Copy the example environment file
   cp .env_example .env
   ```
   Then edit `.env` and add your configurations:
   ```
   MAPBOX_ACCESS_TOKEN=your_mapbox_token_here
   WHISPER_MODEL_PATH=your_whisper_model_path_here
   SPACY_MODEL_PATH=your_spacy_model_path_here
   OLLAMA_API_URL=http://localhost:11434
   ```
   - You can get a Mapbox access token by signing up at https://www.mapbox.com/
   - You can download the Whisper model from https://github.com/openai/whisper
   - You can download the SpaCy model from https://github.com/explosion/spacy-models
   - Update the OLLAMA_API_URL if your Ollama instance is running on a different address

2. **Enable GPU Support (Optional)**

   If using CUDA:

   ```bash
   uv pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
   ```

3. **Install pre-commit:**
   ```bash
   uv pip install pre-commit
   ```
   Pre-commit helps maintain code quality by running automated checks before commits are made.

4. **Install git hooks:**
   ```bash
   pre-commit install --hook-type commit-msg --hook-type pre-commit --hook-type pre-push
   ```

   These hooks perform different checks at various stages:
   - `commit-msg`: Ensures commit messages follow the conventional format
   - `pre-commit`: Runs Ruff linting and formatting checks before each commit
   - `pre-push`: Performs final validation before pushing to remote
  
5. **Code Linting:**
   ```bash
   ruff check
   ruff format
   ```

6. **Run the application:**
   ```bash
   streamlit src/app.py
   ```

---

<div align="center">
  <h2>📝 File Structure</h2>
</div>

```text
📦AeroLex
 ┣ 📂READ.assets
 ┣ 📂src
 ┃ ┣ 📂components
 ┃ ┣ 📂data
 ┃ ┣ 📂models
 ┃ ┣ 📂pages
 ┃ ┣ 📂utils
 ┃ ┗ 📄app.py
 ┣ 📄.env_example
 ┣ 📄.gitignore
 ┣ 📄.pre-commit-config.yaml
 ┣ 📄.pre-commit_msg_template.py
 ┣ 📄LICENSE
 ┗ 📄README.md
```

---

<div align="center">
  <h2>🤝 Contributing</h2>
</div>

We welcome contributions! To contribute:

1. Fork the repository
2. Create a new branch (`feature/branch_name`)
3. Commit changes and push to your fork
4. Submit a Pull Request (PR)
