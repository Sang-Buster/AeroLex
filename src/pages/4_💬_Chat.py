import streamlit as st
from ollama import Client

from components.sidebar import sidebar


def initialize_chat_history():
    if "messages" not in st.session_state:
        st.session_state.messages = []


def initialize_chat_config():
    if "chat_config" not in st.session_state:
        st.session_state.chat_config = {
            "model": "llama2",
            "temperature": 0.8,
            "top_p": 0.9,
            "top_k": 40,
            "num_ctx": 2048,
            "repeat_last_n": 64,
            "repeat_penalty": 1.1,
            "seed": 0,
            "num_predict": -1,
            "min_p": 0.05,
            "mirostat": 0,
            "mirostat_eta": 0.1,
            "mirostat_tau": 5.0,
        }


def update_chat_model():
    """Callback function to update the model in session state"""
    st.session_state.chat_config["model"] = st.session_state.model_selectbox


def get_available_models():
    """Get available Ollama models with their sizes"""
    try:
        # Use get method with default fallback for secrets
        ollama_api_url = st.secrets.get("OLLAMA_API_URL", "http://localhost:11434")

        # Skip the connection test that was causing extra error messages
        # Just try to connect directly to the API
        client = Client(host=ollama_api_url)

        try:
            response = client.list()

            # Extract model names and details
            available_models = []
            model_details = {}

            if hasattr(response, "models") and response.models:
                for model in response.models:
                    available_models.append(model.model)
                    size_gb = model.size / (1024 * 1024 * 1024)  # Convert to GB
                    model_details[model.model] = f"{model.model} ({size_gb:.1f}GB)"

            if not available_models:
                st.warning(
                    "No Ollama models found. Please download at least one model."
                )
                return ["None"], {"None": "No models available"}

            return available_models, model_details

        except Exception as api_error:
            st.error(f"Error fetching models from Ollama: {str(api_error)}")
            st.info("API connection succeeded but model list retrieval failed.")
            return ["None"], {"None": "API Error"}

    except KeyError:
        # Handle case when OLLAMA_API_URL is not in secrets
        st.info("OLLAMA_API_URL not found in secrets, using default localhost:11434")
        try:
            client = Client(host="http://localhost:11434")
            response = client.list()

            # Extract model names and details
            available_models = []
            model_details = {}

            if hasattr(response, "models") and response.models:
                for model in response.models:
                    available_models.append(model.model)
                    size_gb = model.size / (1024 * 1024 * 1024)  # Convert to GB
                    model_details[model.model] = f"{model.model} ({size_gb:.1f}GB)"

            if not available_models:
                st.warning(
                    "No Ollama models found. Please download at least one model."
                )
                return ["None"], {"None": "No models available"}

            return available_models, model_details
        except Exception as inner_e:
            st.error(f"Failed to connect to local Ollama API: {str(inner_e)}")
            st.info(
                "Make sure Ollama is running locally or port forwarding is correctly set up."
            )
            return ["None"], {"None": "Connection Error"}

    except Exception as e:
        error_msg = str(e)
        st.error(f"Failed to connect to Ollama API: {error_msg}")

        # Provide a single, clear instruction instead of multiple messages
        st.info(
            "Check that Ollama is running and accessible. For remote connections, verify your port forwarding setup (e.g., ssh -L 11434:remote:11434)."
        )

        return ["None"], {"None": "Connection Error"}


def chat_interface():
    st.markdown("<h1 style='text-align: center;'>LLM Chat</h1>", unsafe_allow_html=True)

    # Initialize states
    initialize_chat_history()
    initialize_chat_config()

    # Model selection and parameters in main panel
    available_models, model_details = get_available_models()

    # Find the correct index for the current model
    default_index = 0
    if st.session_state.chat_config["model"] in available_models:
        default_index = available_models.index(st.session_state.chat_config["model"])
    elif available_models and available_models[0] != "None":
        # If model not found and we have valid models, update session state
        st.session_state.chat_config["model"] = available_models[0]

    # Use on_change callback to update the model
    st.selectbox(
        "Select Model",
        options=available_models,
        format_func=lambda x: model_details.get(x, x),
        index=default_index,
        key="model_selectbox",
        on_change=update_chat_model,
        help="Select the Ollama model for chat",
    )

    # Display current model for debugging
    st.caption(f"Current model: {st.session_state.chat_config['model']}")

    with st.expander("Model Parameters", expanded=False):
        st.subheader("Basic Parameters")
        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=2.0,
            value=st.session_state.chat_config["temperature"],
            step=0.1,
            help="Higher values make the output more random, lower values make it more deterministic",
        )

        top_p = st.slider(
            "Top P",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state.chat_config["top_p"],
            step=0.1,
            help="Works together with top-k. Higher values lead to more diverse text",
        )

        top_k = st.slider(
            "Top K",
            min_value=1,
            max_value=100,
            value=st.session_state.chat_config["top_k"],
            step=1,
            help="Reduces the probability of generating nonsense",
        )

        min_p = st.slider(
            "Min P",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state.chat_config["min_p"],
            step=0.01,
            help="Minimum probability threshold for token consideration",
        )

        st.subheader("Context & Prediction")
        num_ctx = st.slider(
            "Context Length",
            min_value=512,
            max_value=8192,
            value=st.session_state.chat_config["num_ctx"],
            step=512,
            help="The maximum number of tokens to consider for context",
        )

        num_predict = st.number_input(
            "Max Tokens to Predict",
            min_value=-1,
            max_value=4096,
            value=st.session_state.chat_config["num_predict"],
            help="Maximum number of tokens to predict (-1 for infinite)",
        )

        st.subheader("Repetition Control")
        repeat_last_n = st.slider(
            "Repeat Last N",
            min_value=0,
            max_value=256,
            value=st.session_state.chat_config["repeat_last_n"],
            help="Number of tokens to look back for repetition (0 to disable)",
        )

        repeat_penalty = st.slider(
            "Repeat Penalty",
            min_value=0.0,
            max_value=2.0,
            value=st.session_state.chat_config["repeat_penalty"],
            step=0.1,
            help="Penalty for repeating tokens",
        )

        seed = st.number_input(
            "Random Seed",
            min_value=0,
            max_value=2**32 - 1,
            value=st.session_state.chat_config["seed"],
            help="Random seed for reproducibility (0 for random)",
        )

        st.subheader("Mirostat Settings")
        mirostat = st.selectbox(
            "Mirostat Mode",
            options=[0, 1, 2],
            index=st.session_state.chat_config["mirostat"],
            help="Mirostat sampling mode (0=disabled, 1=Mirostat, 2=Mirostat 2.0)",
        )

        if mirostat > 0:
            mirostat_tau = st.slider(
                "Mirostat Tau",
                min_value=0.0,
                max_value=10.0,
                value=st.session_state.chat_config["mirostat_tau"],
                step=0.1,
                help="Controls output randomness in Mirostat",
            )

            mirostat_eta = st.slider(
                "Mirostat Eta",
                min_value=0.0,
                max_value=1.0,
                value=st.session_state.chat_config["mirostat_eta"],
                step=0.01,
                help="Learning rate for Mirostat",
            )

    # Update config with all parameters
    st.session_state.chat_config.update(
        {
            "model": st.session_state.chat_config["model"],
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k,
            "min_p": min_p,
            "num_ctx": num_ctx,
            "num_predict": num_predict,
            "repeat_last_n": repeat_last_n,
            "repeat_penalty": repeat_penalty,
            "mirostat": mirostat,
            "mirostat_tau": mirostat_tau if mirostat > 0 else 5.0,
            "mirostat_eta": mirostat_eta if mirostat > 0 else 0.1,
            "seed": seed,
        }
    )

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Send a message"):
        # Display user message
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        try:
            # Display assistant response with streaming
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""

                # Create Ollama client with custom host if specified
                client = Client(
                    host=st.secrets.get("OLLAMA_API_URL", "http://localhost:11434")
                )
                stream = client.chat(
                    model=st.session_state.chat_config["model"],
                    messages=[
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ],
                    stream=True,
                    options={
                        "temperature": st.session_state.chat_config["temperature"],
                        "top_p": st.session_state.chat_config["top_p"],
                        "top_k": st.session_state.chat_config["top_k"],
                        "min_p": st.session_state.chat_config["min_p"],
                        "num_ctx": st.session_state.chat_config["num_ctx"],
                        "num_predict": st.session_state.chat_config["num_predict"],
                        "repeat_last_n": st.session_state.chat_config["repeat_last_n"],
                        "repeat_penalty": st.session_state.chat_config[
                            "repeat_penalty"
                        ],
                        "mirostat": st.session_state.chat_config["mirostat"],
                        "mirostat_tau": st.session_state.chat_config["mirostat_tau"],
                        "mirostat_eta": st.session_state.chat_config["mirostat_eta"],
                        "seed": st.session_state.chat_config["seed"],
                    },
                )

                # Stream the response
                for chunk in stream:
                    if chunk and "message" in chunk and "content" in chunk["message"]:
                        full_response += chunk["message"]["content"]
                        message_placeholder.markdown(full_response + "▌")

                message_placeholder.markdown(full_response)

            # Add assistant response to chat history
            st.session_state.messages.append(
                {"role": "assistant", "content": full_response}
            )

        except Exception as e:
            st.error(f"Error generating response: {str(e)}")
            st.info(
                "Please make sure Ollama is running locally and the selected model is downloaded."
            )


def llm_chat_page():
    sidebar()
    chat_interface()


if __name__ == "__main__":
    llm_chat_page()
