import argparse
import subprocess
import sys

import spacy


def is_model_installed(model_name):
    """Check if the given spaCy model is installed"""
    return spacy.util.is_package(model_name)


def download_model(model_size):
    """Download the specified spaCy model if not already installed"""
    model_map = {
        "sm": "en_core_web_sm",
        "md": "en_core_web_md",
        "lg": "en_core_web_lg",
        "trf": "en_core_web_trf",
    }

    if model_size not in model_map:
        print(
            f"Invalid model size '{model_size}'. Choose from 'sm', 'md', 'lg', or 'trf'."
        )
        return

    model_name = model_map[model_size]

    if is_model_installed(model_name):
        print(f"Model '{model_name}' is already installed.")
    else:
        try:
            print(f"Downloading spaCy model '{model_name}'...")
            subprocess.run(
                [sys.executable, "-m", "spacy", "download", model_name], check=True
            )
            print(f"Model '{model_name}' downloaded successfully.")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while downloading the model: {e}")


def test_model(model_size):
    """Test the specified spaCy model by running a sample sentence"""
    model_map = {
        "sm": "en_core_web_sm",
        "md": "en_core_web_md",
        "lg": "en_core_web_lg",
        "trf": "en_core_web_trf",
    }

    if model_size not in model_map:
        print(
            f"Invalid model size '{model_size}'. Choose from 'sm', 'md', 'lg', or 'trf'."
        )
        return

    model_name = model_map[model_size]

    if not is_model_installed(model_name):
        print(
            f"Model '{model_name}' is not installed. Run 'python script.py download {model_size}' first."
        )
        return

    print(f"Testing spaCy model '{model_name}'...")
    try:
        nlp = spacy.load(model_name)
        doc = nlp("This is a test sentence.")
        for token in doc:
            print(token.text, token.pos_, token.dep_)
        print("=" * 50)
        print(f"Model '{model_name}' tested successfully.")
        print("=" * 50)
    except Exception as e:
        print(f"Error testing the model: {e}")


def show_installed_models():
    """Show all installed spaCy models and their paths"""
    print("Checking installed spaCy models...\n")
    installed_models = spacy.info().get("pipelines", {})

    if installed_models:
        for model_name, details in installed_models.items():
            print(f"Model: {model_name}")

            # Ensure details is a dictionary before accessing keys
            if isinstance(details, dict):
                version = details.get("version", "Unknown")
            else:
                version = "Unknown"

            print(f"  Version: {version}")
            print(f"  Path: {spacy.util.get_package_path(model_name)}\n")
    else:
        print("No spaCy models found.")


def remove_model(model_size):
    """Remove the specified spaCy model properly"""
    model_map = {
        "sm": "en_core_web_sm",
        "md": "en_core_web_md",
        "lg": "en_core_web_lg",
        "trf": "en_core_web_trf",
    }

    if model_size not in model_map:
        print(
            f"Invalid model size '{model_size}'. Choose from 'sm', 'md', 'lg', or 'trf'."
        )
        return

    model_name = model_map[model_size]

    if not is_model_installed(model_name):
        print(f"Model '{model_name}' is not installed.")
        return

    try:
        print(f"Uninstalling spaCy model '{model_name}'...")
        subprocess.run(
            [sys.executable, "-m", "pip", "uninstall", "-y", model_name], check=True
        )
        print(f"Model '{model_name}' has been successfully removed.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to uninstall model: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manage spaCy language models.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Sub-command for downloading a model
    download_parser = subparsers.add_parser("download", help="Download a spaCy model")
    download_parser.add_argument(
        "size",
        choices=["sm", "md", "lg", "trf"],
        help="Model size: 'sm', 'md', 'lg', 'trf'",
    )

    # Sub-command for testing a model
    test_parser = subparsers.add_parser("test", help="Test a spaCy model")
    test_parser.add_argument(
        "size",
        choices=["sm", "md", "lg", "trf"],
        help="Model size: 'sm', 'md', 'lg', 'trf'",
    )

    # Sub-command for showing installed models
    show_parser = subparsers.add_parser("show", help="Show installed spaCy models")

    # Sub-command for removing a model
    remove_parser = subparsers.add_parser("remove", help="Remove a spaCy model")
    remove_parser.add_argument(
        "size",
        choices=["sm", "md", "lg", "trf"],
        help="Model size: 'sm', 'md', 'lg', 'trf'",
    )

    args = parser.parse_args()

    if args.command == "download":
        download_model(args.size)
    elif args.command == "test":
        test_model(args.size)
    elif args.command == "show":
        show_installed_models()
    elif args.command == "remove":
        remove_model(args.size)
