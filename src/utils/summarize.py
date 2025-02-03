"""Real-time summarization utility using Ollama directly"""

import json
import logging
import os
from datetime import datetime
from typing import List, Optional

import ollama
import streamlit as st
from pydantic import BaseModel, Field

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Communication(BaseModel):
    """A single ATC communication"""

    speaker: Optional[str] = Field(
        None, description="Who is speaking (if identifiable)"
    )
    recipient: Optional[str] = Field(
        None, description="Who they're speaking to (if identifiable)"
    )
    instruction: Optional[str] = Field(
        None, description="Any specific instruction given"
    )
    location: Optional[str] = Field(None, description="Any location mentioned")
    altitude: Optional[str] = Field(None, description="Any altitude mentioned")
    heading: Optional[str] = Field(None, description="Any heading mentioned")
    action: Optional[str] = Field(None, description="Action requested or acknowledged")


class ATCSummary(BaseModel):
    """ATC communication summary with structured data"""

    title: str = Field(
        ..., description="Brief description of the main communication context"
    )
    tldr: str = Field(..., description="One-line summary of key events")
    communications: List[Communication] = Field(
        ..., description="Array of identified communications"
    )
    details: Optional[str] = Field(
        None, description="Additional relevant information not captured above"
    )


class OllamaSummarizer:
    def __init__(self, model_name="llama3.2:3b-instruct-q4_K_M"):
        try:
            # Initialize Ollama client with custom API URL from secrets
            api_url = st.secrets["OLLAMA_API_URL"]
            logger.info(f"Connecting to Ollama at: {api_url}")
            self.client = ollama.Client(host=api_url)

            # Test connection and check if model exists
            response = self.client.list()
            logger.info(f"API Response: {response}")

            # Extract model names from the response
            available_models = []
            if hasattr(response, "models"):
                available_models = [model.model for model in response.models]
            elif isinstance(response, dict) and "models" in response:
                available_models = [model.get("model") for model in response["models"]]
            else:
                available_models = [model.model for model in response]

            logger.info(f"Available models: {available_models}")

            if not available_models:
                logger.warning("No models found in response")
                available_models = [model_name]

            if model_name not in available_models:
                raise ValueError(
                    f"Model {model_name} not found. Available models: {available_models}"
                )

            logger.info("Successfully connected to Ollama server")
            self.model = model_name

            # Set up summary output path in text folder
            self.output_dir = os.path.join("src", "data", "text")
            os.makedirs(self.output_dir, exist_ok=True)
            self.summary_path = os.path.join(
                self.output_dir,
                f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            )

        except Exception as e:
            logger.error(f"Failed to initialize Ollama client: {str(e)}")
            st.error(f"""
                Failed to connect to Ollama server at {api_url}.
                Please check:
                1. SSH tunnel is active: `ssh -L 11434:localhost:11434 user@hpc`
                2. Ollama server is running on HPC: `ollama serve`
                3. API URL is correct in .streamlit/secrets.toml
                4. Model {model_name} is available
                
                Available models: {available_models if "available_models" in locals() else "Unknown"}
                Error: {str(e)}
            """)
            raise

    def save_summary(self, summary: dict):
        """Save the summary to a JSON file"""
        try:
            with open(self.summary_path, "w", encoding="utf-8") as f:
                json.dump(summary, f, indent=2, ensure_ascii=False)
            logger.info(f"Summary saved to {self.summary_path}")
        except Exception as e:
            logger.error(f"Failed to save summary: {str(e)}")

    def summarize(self, text: str) -> dict:
        """Summarize ATC communications using structured output"""
        summary = None
        if not text.strip():
            summary = ATCSummary(
                title="No content yet",
                tldr="Waiting for content...",
                communications=[],
                details="Start speaking to see the summary.",
            ).model_dump()
            self.save_summary(summary)
            return summary

        try:
            logger.info(f"Sending request to Ollama model: {self.model}")

            # Create a structured prompt with JSON schema
            prompt = f"""
            You are an expert ATC communication analyzer. Analyze the following transcript and provide a response in the exact JSON format shown below.
            For short ATC communications, make reasonable assumptions based on standard ATC protocols, but clearly mark inferred information.

            IMPORTANT: Ensure the response is valid JSON with all property names and string values enclosed in double quotes.

            The response must strictly follow this schema:
            {{
                "title": "Brief description of the main communication context",
                "tldr": "One-line summary of key events",
                "communications": [
                    {{
                        "speaker": "Who is speaking (if identifiable, prefix with [Inferred] if guessed)",
                        "recipient": "Who they're speaking to (if identifiable)",
                        "instruction": "Any specific instruction given",
                        "location": "Any location mentioned",
                        "altitude": "Any altitude mentioned",
                        "heading": "Any heading mentioned",
                        "action": "Action requested or acknowledged"
                    }}
                ],
                "details": "Additional relevant information including any assumptions made"
            }}

            Guidelines:
            1. For explicit information in the transcript, provide it directly
            2. For short ATC communications:
               - Make reasonable assumptions based on standard ATC protocols
               - Prefix inferred information with "[Inferred]"
               - Explain assumptions in the details field
            3. For heading instructions, include both numeric and cardinal directions
            4. Include context about the phase of flight if it can be reasonably inferred
            5. Provide the response as a single, valid JSON object
            6. Ensure all property names and string values are enclosed in double quotes

            Transcript to analyze:
            {text}
            """

            response = self.client.generate(
                model=self.model, prompt=prompt, stream=False
            )

            logger.info("Received response from Ollama")
            response_text = response.response.strip()

            # Try to find and extract JSON content
            try:
                # Look for content between first { and last }
                start_idx = response_text.find("{")
                end_idx = response_text.rindex("}") + 1
                if start_idx != -1 and end_idx != -1:
                    json_str = response_text[start_idx:end_idx]
                    parsed_data = json.loads(json_str)
                else:
                    raise ValueError("No JSON object found in response")
            except json.JSONDecodeError as json_err:
                logger.error(f"JSON parsing error: {str(json_err)}")
                logger.error(f"Response text: {response_text}")
                raise

            # Validate with Pydantic
            try:
                validated_summary = ATCSummary.model_validate(parsed_data)
            except Exception as pydantic_err:
                logger.error(f"Pydantic validation error: {str(pydantic_err)}")
                # Attempt to create a minimal valid summary
                summary = ATCSummary(
                    title="Parsing Error",
                    tldr="Failed to parse LLM response",
                    communications=[],
                    details=f"Error: {str(pydantic_err)}\nRaw response: {response_text}",
                ).model_dump()
            else:
                summary = validated_summary.model_dump()
            self.save_summary(summary)
            return summary

        except Exception as e:
            logger.error(f"Error during summarization: {str(e)}")
            summary = ATCSummary(
                title="Error in summarization",
                tldr=f"Error: {str(e)}",
                communications=[
                    Communication(
                        speaker="System",
                        action="Error occurred while summarizing",
                        details=f"Model used: {self.model}",
                    )
                ],
                details=f"""
                Please check:
                1. SSH tunnel is active: ssh -L 11434:localhost:11434 user@hpc
                2. Ollama is running on HPC: ollama serve
                3. Model {self.model} is available: ollama list
                
                Full error: {str(e)}
                """,
            ).model_dump()
            self.save_summary(summary)
            return summary
