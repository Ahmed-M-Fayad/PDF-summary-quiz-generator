import streamlit as st
import requests
from typing import List, Dict, Any, Optional

def create_sidebar(model_name: str = "llama3:latest"):
    """Create an informative sidebar with model info and manual text input options."""
    
    with st.sidebar:
        st.title("📋 Tools & Info")
        
        # Add collapsible sections for better organization
        with st.expander("ℹ️ About", expanded=True):
            st.markdown("""
            **PDF Quiz & Summary Generator** helps you quickly extract knowledge from PDF documents.
            
            - 📑 **Generate detailed summaries** of any PDF
            - 🧠 **Create interactive quizzes** to test understanding
            - 📝 **Process manual text input** for quick summaries
            """)
        
        # Model information section
        with st.expander("🤖 Model Information", expanded=True):
            model_info = get_model_info(model_name)
            
            if model_info:
                st.success(f"✅ Using: **{model_name}**")
                
                # Display additional model details if available
                if "parameters" in model_info:
                    st.metric("Model Parameters", f"{model_info['parameters']/1_000_000_000:.1f}B")
                
                if "family" in model_info:
                    st.info(f"Model Family: {model_info['family']}")
                
                # Show model capabilities as tags
                if "tags" in model_info and model_info["tags"]:
                    st.markdown("**Capabilities:**")
                    tags_html = ""
                    for tag in model_info["tags"]:
                        tags_html += f'<span style="background-color: #9575CD; color: white; padding: 2px 6px; margin-right: 5px; border-radius: 10px; font-size: 0.8em;">{tag}</span>'
                    st.markdown(f'<div style="margin-top: 5px;">{tags_html}</div>', unsafe_allow_html=True)
            else:
                st.warning(f"⚠️ Model info unavailable for **{model_name}**")
                st.markdown("Make sure Ollama is running with the correct model.")
        
        # Add manual text input section
        with st.expander("📝 Manual Text Input", expanded=False):
            st.markdown("**Summarize text without uploading PDF**")
            
            manual_text = st.text_area(
                "Enter or paste text to summarize:",
                height=200,
                help="Enter any text you want to summarize without uploading a PDF"
            )
            
            if manual_text:
                st.session_state.manual_text = manual_text
                
                if st.button("Generate Summary", key="sidebar_summary_btn"):
                    with st.spinner("Generating summary from text input..."):
                        if len(manual_text.strip()) < 50:
                            st.error("Please enter more text (at least 50 characters)")
                        else:
                            # Store the text in session state to be processed
                            st.session_state.manual_input_for_summary = manual_text
                            st.success("Text ready for summarization!")
                            st.session_state.show_manual_summary = True
                            # The actual summarization will be handled in main app
                            st.rerun()

        # Dark/Light mode toggle (conceptual - actual implementation would need additional work)
        theme_col1, theme_col2 = st.columns(2)
        
        with theme_col1:
            if st.button("🌙 Dark"):
                st.session_state.dark_mode = True
                st.rerun()
        
        with theme_col2:
            if st.button("☀️ Light"):
                st.session_state.dark_mode = False
                st.rerun()
        
        # Helpful resources
        with st.expander("📚 Resources", expanded=False):
            st.markdown("""
            - [Ollama Documentation](https://ollama.ai/docs)
            - [PDF Processing Tips](https://streamlit.io/gallery?category=pdf-processing)
            - [Teaching with AI](https://www.unesco.org/en/artificial-intelligence/education)
            """)
        
        # Footer with app version
        st.markdown("---")
        st.markdown(
            "<div style='text-align: center; color: #888; font-size: 0.8em;'>Version 1.1.0</div>", 
            unsafe_allow_html=True
        )

def get_model_info(model_name: str) -> Optional[Dict[str, Any]]:
    """
    Fetch model information from Ollama API.
    
    Args:
        model_name: Name of the model to fetch info for
        
    Returns:
        Dictionary with model information or None if unavailable
    """
    try:
        response = requests.get("http://localhost:11434/api/tags")
        if response.status_code == 200:
            data = response.json()
            
            # Find the requested model in the list
            for model in data.get("models", []):
                if model["name"] == model_name:
                    # Construct a more useful info object
                    info = {
                        "name": model_name,
                        "size": model.get("size", "Unknown"),
                        "modified_at": model.get("modified_at", "Unknown"),
                        "parameters": 7_000_000_000,  # Default for llama3:latest (change as needed)
                        "family": "LLaMA",
                        "tags": ["Summarization", "Question Answering", "Content Generation"]
                    }
                    return info
        
        return None
    except requests.RequestException:
        return None