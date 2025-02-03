import os
from datetime import datetime

import streamlit as st

from components.sidebar import sidebar
from components.text_visualizer import visualize_ner, visualize_parser, visualize_tokens
from models.spacy_models import is_model_installed
from utils.text_processing import load_nlp_model, process_text

# Available spaCy models
SPACY_MODELS = {
    "": None,  # Empty default option
    "Small (12MB)": "en_core_web_sm",
    "Medium (310MB)": "en_core_web_md",
    "Large (382MB)": "en_core_web_lg",
    "Transformer (436MB)": "en_core_web_trf",
}


def save_text_file(text_content):
    """Save text to file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"text_{timestamp}.txt"
    save_path = os.path.join("src/data/text", filename)

    # Ensure directory exists
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    with open(save_path, "w", encoding="utf-8") as f:
        f.write(text_content)
    return save_path


def text_page():
    sidebar()

    st.markdown(
        "<h1 style='text-align: center;'>Text Processing</h1>", unsafe_allow_html=True
    )

    # Initialize all session state variables
    if "text_content" not in st.session_state:
        st.session_state.text_content = None
    if "saved_path" not in st.session_state:
        st.session_state.saved_path = None
    if "nlp" not in st.session_state:
        st.session_state.nlp = None
    if "current_model" not in st.session_state:
        st.session_state.current_model = None

    # Model selection
    model_name = st.selectbox(
        "Select SpaCy Model",
        options=list(SPACY_MODELS.keys()),
        index=0,  # Set default to first option (empty)
        help="Choose a model size. Larger models are more accurate but slower.",
    )

    if not model_name:  # If no model is selected
        st.info("👆 Please select a model to start processing text")
        st.stop()

    selected_model = SPACY_MODELS[model_name]

    # Check if selected model is installed
    if not is_model_installed(selected_model):
        st.error(
            f"Model '{selected_model}' is not installed. "
            f"Please run the following command to install it:\n\n"
            f"```bash\npython src/models/spacy_models.py download {selected_model.split('_')[-1]}\n```"
        )
        st.stop()

    # Load spaCy model only when a different model is selected
    if selected_model != st.session_state.current_model:
        try:
            st.session_state.nlp = load_nlp_model(selected_model)
            st.session_state.current_model = selected_model
            st.success(f"Successfully loaded {model_name} model")
        except Exception as e:
            st.error(f"Error loading model: {str(e)}")
            st.stop()

    # Text input methods
    text_input = st.text_area(
        "Enter text to analyze",
        height=200,
        help="Type, paste text, or upload a file below",
    )

    uploaded_file = st.file_uploader(
        "Or upload a text file",
        type=["txt", "xml"],
        help="Upload a text file to analyze",
    )

    # Process text when there's input
    new_content = False
    if uploaded_file:
        text_content = uploaded_file.getvalue().decode("utf-8")
        if text_content != st.session_state.text_content:
            st.session_state.text_content = text_content
            new_content = True
    elif text_input and text_input.strip():
        if text_input != st.session_state.text_content:
            st.session_state.text_content = text_input
            new_content = True

    if st.session_state.text_content:
        # Only save if it's new content
        if new_content:
            save_path = save_text_file(st.session_state.text_content)
            st.session_state.saved_path = save_path
            st.success(f"Text saved to {save_path}")

        # Process text with spaCy
        with st.spinner(f"Processing text with {model_name} model..."):
            doc = process_text(st.session_state.text_content, st.session_state.nlp)

        # Model information
        with st.expander("Model Information", expanded=False):
            vectors_data = st.session_state.nlp.vocab.vectors.data
            has_vectors = (
                vectors_data.size > 0 if hasattr(vectors_data, "size") else False
            )
            n_vectors = (
                st.session_state.nlp.vocab.vectors.n_vectors if has_vectors else 0
            )
            vector_dim = (
                st.session_state.nlp.vocab.vectors.shape[1] if has_vectors else 0
            )

            st.write(f"""
            - **Model**: {model_name} ({selected_model})
            - **Pipeline Components**: {", ".join(st.session_state.nlp.pipe_names)}
            - **Word Vectors**: {"✓ Included" if has_vectors else "Not included"}
            {f"  - Number of words with vectors: {n_vectors:,}" if has_vectors else ""}
            {f"  - Vector dimensions: {vector_dim}" if has_vectors else ""}
            
            💡 **Note**: 
            - Small model (sm) doesn't include word vectors
            - Medium model (md) includes 685k keys, 20k unique vectors (300 dimensions)
            - Large model (lg) includes 685k keys, 343k unique vectors (300 dimensions)
            - Transformer model (trf) uses contextual embeddings
            """)

        # Visualization sections
        st.markdown("---")

        # Dependency Parsing
        st.subheader("Dependency Parsing")
        visualize_parser(doc)

        # Named Entity Recognition
        st.markdown("---")
        st.subheader("Named Entity Recognition")
        visualize_ner(doc)

        # Token Analysis
        st.markdown("---")
        st.subheader("Token Analysis")
        visualize_tokens(doc)


if __name__ == "__main__":
    text_page()
