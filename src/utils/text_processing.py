"""Text processing utilities"""

from typing import Optional

import spacy


def load_nlp_model(model_name: str = "en_core_web_sm") -> spacy.language.Language:
    """Load spaCy model"""
    return spacy.load(model_name)


def process_text(
    text: str, nlp: Optional[spacy.language.Language] = None
) -> spacy.tokens.Doc:
    """Process text with spaCy"""
    if nlp is None:
        nlp = load_nlp_model()
    return nlp(text)


def get_svg_html(svg: str) -> str:
    """Convert SVG to HTML for display"""
    html_wrapper = """<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem; margin-bottom: 2.5rem">{}</div>"""
    return html_wrapper.format(svg)
