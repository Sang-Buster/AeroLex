import streamlit as st


def display_transcription(transcription: str):
    """Display the transcription in a scrollable container"""
    st.markdown(
        f"""
        <div style="height: 500px; overflow-y: auto; padding: 10px;">
            {transcription.replace("\n", "<br>")}
        </div>
        """,
        unsafe_allow_html=True,
    )


def display_summary(summary: dict):
    """Display the ATC communication summary"""
    if not summary:
        return

    # Use Streamlit's native container
    with st.container():
        # Title and TLDR section
        if summary.get("title"):
            st.markdown(f"#### {summary['title']}")

        if summary.get("tldr"):
            st.markdown(f"*{summary['tldr']}*")
            st.markdown("---")

        # Communications section
        if summary.get("communications"):
            for comm in summary["communications"]:
                # Speaker and Recipient
                parts = []
                if comm.get("speaker"):
                    parts.append(f"**From:** {comm['speaker']}")
                if comm.get("recipient"):
                    parts.append(f"**To:** {comm['recipient']}")
                if parts:
                    st.markdown(" | ".join(parts))

                # Instructions and Actions
                if comm.get("instruction"):
                    st.markdown(f"**Instruction:** {comm['instruction']}")
                if comm.get("action"):
                    st.markdown(f"**Action:** {comm['action']}")

                # Location, Altitude, Heading
                if comm.get("location"):
                    st.markdown(f"**Location:** {comm['location']}")
                if comm.get("altitude"):
                    st.markdown(f"**Altitude:** {comm['altitude']}")
                if comm.get("heading"):
                    st.markdown(f"**Heading:** {comm['heading']}")

                st.markdown("---")

        # Details section
        if summary.get("details"):
            st.markdown("**Additional Details:**")
            st.markdown(summary["details"])
