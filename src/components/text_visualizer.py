from typing import Dict, List, Optional

import pandas as pd
import spacy
import streamlit as st
from spacy import displacy

from utils.text_processing import get_svg_html

# Define a color scheme
ENTITY_COLORS: Dict[str, str] = {
    "PERSON": "#F67DE3",
    "ORG": "#7AECEC",
    "GPE": "#BFEEB7",
    "LOC": "#9CC9F0",
    "DATE": "#FFB59B",
    "TIME": "#FF9561",
    "MONEY": "#E4E7D2",
    "PERCENT": "#C887FB",
    "PRODUCT": "#9DEEF0",
    "EVENT": "#FF8197",
    "NORP": "#C887FB",
    "LANGUAGE": "#FFB4B4",
    "LAW": "#B4FFB4",
    "WORK_OF_ART": "#FFB4FF",
    "FAC": "#B4B4FF",
    "QUANTITY": "#FF9561",
}


def visualize_parser(doc: spacy.tokens.Doc, options: dict = None) -> None:
    """Visualize dependency parsing"""
    if options is None:
        options = {}

    # Parser visualization controls
    cols = st.columns(3)
    options.update(
        {
            "collapse_punct": cols[0].checkbox("Collapse punctuation", value=True),
            "collapse_phrases": cols[1].checkbox("Collapse phrases"),
            "compact": cols[2].checkbox("Compact mode"),
        }
    )

    # Generate and display the dependency visualization
    svg = displacy.render(doc, style="dep", options=options)
    st.write(get_svg_html(svg), unsafe_allow_html=True)


def visualize_ner(doc: spacy.tokens.Doc, labels: Optional[List[str]] = None) -> None:
    """Visualize named entities"""
    if not doc.ents:
        st.warning("No named entities found in the text.")
        return

    # Get unique entity labels from the doc if not provided
    if labels is None:
        labels = list({ent.label_ for ent in doc.ents})

    # Entity label selection
    selected_labels = st.multiselect(
        "Entity labels",
        options=labels,
        default=labels,
        help="Select which types of entities to display",
    )

    # Colors for different entity types
    colors = {label: ENTITY_COLORS.get(label, "#E4E7D2") for label in labels}

    options = {"ents": selected_labels, "colors": colors}

    # Generate and display the NER visualization
    html = displacy.render(doc, style="ent", options=options)
    st.write(get_svg_html(html), unsafe_allow_html=True)

    # Display entities in a table
    if doc.ents:
        data = [
            [ent.text, ent.label_, ent.start_char, ent.end_char]
            for ent in doc.ents
            if ent.label_ in selected_labels
        ]
        if data:
            df = pd.DataFrame(data, columns=["Text", "Label", "Start", "End"])
            st.dataframe(df)


def visualize_tokens(doc: spacy.tokens.Doc) -> None:
    """Visualize token attributes"""
    attrs = ["text", "lemma_", "pos_", "tag_", "dep_", "shape_", "is_alpha", "is_stop"]

    # Token attribute selection
    selected_attrs = st.multiselect(
        "Token attributes",
        options=attrs,
        default=["text", "lemma_", "pos_", "tag_", "dep_"],
        help="Select token attributes to display",
    )

    # Create and display tokens dataframe
    data = [[getattr(token, attr) for attr in selected_attrs] for token in doc]
    df = pd.DataFrame(data, columns=selected_attrs)
    st.dataframe(df)
