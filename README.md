<div align="center">
   <a href="https://github.com/Sang-Buster/AeroLex">
      <img src="/src/assets/favicon.png" width=20% alt="logo">
   </a>   
   <h1>AeroLex</h1>
   <h6><small>Making Airwaves Understandable - An AI-powered ATC Communication Analysis Tool</small></h6>
   <p><b>#LLM &emsp; #Air Traffic Control Communication &emsp; #Automatic Speech Recognition &emsp; #Aviation &emsp; #AI <br/>
   #Name Entity Recognition &emsp; #Speech-to-Text &emsp; #Natural Language Processing &emsp; #Real-time Analysis</b></p>
</div>

---

<div align="center">
  <h2>🔍 Table of Contents</h2>
</div>

- [✨ Features](#-key-features)
- [👨‍💻 Tech Stack](#-tech-stack)
- [🚀 Getting Started](#-getting-started)
- [⚒️ Development Setup](#%EF%B8%8F-development-setup)
- [📝 File Structure](#-file-structure)
- [🤝 Contributing](#-contributing)

---

<div align="center">
  <h2>✨ Key Features</h2>
</div>

AeroLex is an AI-powered web application that transcribes, visualizes, and analyzes air traffic communication. It transforms ATC conversations into structured, actionable insights. Some of the key features are:
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
   touch .streamlit/secrets.toml
   ```
   Then edit `secrets.toml` and add your configurations:
   ```
   MAPBOX_ACCESS_TOKEN = "your_mapbox_token_here"
   WHISPER_MODEL_PATH = "your_whisper_model_path_here"
   SPACY_MODEL_PATH = "your_spacy_model_path_here"
   OLLAMA_API_URL = "http://localhost:11434"
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
   uv pip install ruff pre-commit
   ```
   `pre-commit` helps maintain code quality by running automated checks before commits are made.
   `ruff` is a modern Python code formatter and linter.

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
   ruff check --select I
   ruff check --fix
   ruff check --select I --fix
   ruff format
   ```

6. **Run the application:**
   ```bash
   streamlit run src/🏠_Home.py
   ```

---

<div align="center">
  <h2>📝 File Structure</h2>
</div>

```text
📦AeroLex
 ┣ 📂READ.assets
 ┣ 📂src
 ┃ ┣ 📂assets
 ┃ ┃ ┗ 📄favicon.png
 ┃ ┣ 📂components
 ┃ ┃ ┣ 📄audio_visualizer.py
 ┃ ┃ ┣ 📄sidebar.py
 ┃ ┃ ┣ 📄text_visualizer.py
 ┃ ┃ ┗ 📄transcription_viewer.py
 ┃ ┣ 📂data
 ┃ ┃ ┣ 📂audio
 ┃ ┃ ┗ 📂text
 ┃ ┣ 📂models
 ┃ ┃ ┣ 📄ollama_models.py
 ┃ ┃ ┣ 📄spacy_models.py
 ┃ ┃ ┗ 📄whisper_models.py
 ┃ ┣ 📂pages
 ┃ ┃ ┣ 📄1_🔊_Audio.py
 ┃ ┃ ┣ 📄2_📝_Text.py
 ┃ ┃ ┣ 📄3_💽_Transcribe.py
 ┃ ┃ ┗ 📄4_💬_Chat.py
 ┃ ┣ 📂utils
 ┃ ┃ ┣ 📄audio_processing.py
 ┃ ┃ ┣ 📄model_integration.py
 ┃ ┃ ┣ 📄summarize.py
 ┃ ┃ ┣ 📄text_processing.py
 ┃ ┃ ┗ 📄transcribe.py
 ┃ ┗ 📄🏠_Home.py
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
