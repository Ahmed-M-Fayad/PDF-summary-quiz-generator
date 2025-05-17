import streamlit as st
import logging
from src.pdf_processor import extract_text_from_pdf
from src.summary_generator import generate_summary
from src.quiz_generator import generate_quiz
from src.ui.components import (
    display_interactive_quiz,
    display_summary,
    content_preview,
    display_error,
)
from src.ui.sidebar import create_sidebar
from assets.styles import apply_all_styles
import requests

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ollama model configuration
MODEL_NAME = "llama3:latest"


def main():
    """Main Streamlit app function with enhanced UI and sidebar"""
    # Set page configuration
    st.set_page_config(
        page_title="Quiz & Summary Generator",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="expanded",  # Show sidebar by default now
    )

    # Initialize session state for dark mode
    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = False  # Default to light mode

    # Apply custom styling with dark mode preference
    apply_all_styles(include_dark_mode=st.session_state.dark_mode)

    # Create sidebar with model info and manual text input
    create_sidebar(MODEL_NAME)

    # Main content area
    with st.container():
        # Stylish header with pulsing effect
        st.markdown(
            """
        <div class="app-header" style="animation: pulse 2s infinite ease-in-out;">
            <h1>📚 Quiz & Summary Generator</h1>
            <p style="color: white; margin-top: 0;">Transform PDFs into knowledge with AI assistance</p>
        </div>
        <style>
        @keyframes pulse {
            0% { box-shadow: 0 0 0 0 rgba(156, 39, 176, 0.4); }
            70% { box-shadow: 0 0 0 10px rgba(156, 39, 176, 0); }
            100% { box-shadow: 0 0 0 0 rgba(156, 39, 176, 0); }
        }
        </style>
        """,
            unsafe_allow_html=True,
        )

        # Enhanced Introduction
        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown(
                """
            ### 🔍 Process PDF Documents in Seconds
            
            This tool helps you **extract valuable information** from PDFs by:
            
            1. Generating **comprehensive summaries** of the document's content
            2. Creating **interactive quizzes** to test understanding
            3. Supporting **manual text input** for quick summarization
            
            Perfect for students, educators, and professionals working with documents!
            """
            )

        with col2:
            # Add a decorative image/animation
            st.markdown(
                """
            <div style="display: flex; justify-content: center; margin-top: 20px;">
                <div style="text-align: center; background: linear-gradient(135deg, #9C27B0 0%, #673AB7 100%); 
                            border-radius: 50%; width: 120px; height: 120px; display: flex; 
                            align-items: center; justify-content: center; font-size: 3rem;">
                    📑➡️🧠
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )

        # Check Ollama availability with better styling
        try:
            response = requests.get("http://localhost:11434/api/tags")
            models = [model["name"] for model in response.json()["models"]]
            if MODEL_NAME not in models:
                st.warning(
                    f"⚠️ Model '{MODEL_NAME}' is not available in Ollama. Pull it using: `ollama pull {MODEL_NAME}`"
                )
        except requests.RequestException:
            st.error(
                "❌ Cannot connect to Ollama API. Make sure it's running on port 11434."
            )

        # Create horizontal line to separate sections
        st.markdown(
            "<hr style='margin: 2rem 0; background: linear-gradient(90deg, transparent, #9575CD, transparent);'>",
            unsafe_allow_html=True,
        )

        # File upload section with improved UI
        st.markdown("### 📄 Upload Your Document")

        col_upload1, col_upload2 = st.columns([3, 1])

        with col_upload1:
            uploaded_file = st.file_uploader(
                "Choose a PDF file",
                type=["pdf"],
                help="Upload any PDF document to generate a summary and quiz",
                key="pdf_uploader",
            )

        with col_upload2:
            # Add an information box
            st.markdown(
                """
            <div style="background-color: rgba(149, 117, 205, 0.1); padding: 10px; border-radius: 5px; 
                       border-left: 3px solid #9575CD; margin-top: 25px;">
                <small>Supported: PDF documents up to 50MB</small>
            </div>
            """,
                unsafe_allow_html=True,
            )

        # Process manual text input if requested from sidebar
        if (
            "show_manual_summary" in st.session_state
            and st.session_state.show_manual_summary
        ):
            if "manual_input_for_summary" in st.session_state:
                st.markdown("### 📝 Processing Manual Text Input")

                manual_text = st.session_state.manual_input_for_summary

                with st.expander("View Input Text", expanded=False):
                    st.text_area(
                        "Text Being Processed:",
                        value=manual_text,
                        height=100,
                        disabled=True,
                    )

                # Generate summary for the manual text
                with st.spinner("Generating summary from manual text input..."):
                    summary = generate_summary(manual_text)

                    # Display the summary
                    display_summary(summary)

                # Reset the show flag but keep the text for reference
                st.session_state.show_manual_summary = False

                st.markdown("<hr style='margin: 2rem 0;'>", unsafe_allow_html=True)

        # Process uploaded PDF
        if uploaded_file:
            st.success(f"✅ File uploaded successfully: **{uploaded_file.name}**")

            # Store processed data in session state to preserve it between reruns
            if "quiz_data" not in st.session_state:
                st.session_state.quiz_data = None

            if "summary_text" not in st.session_state:
                st.session_state.summary_text = None

            # Process PDF and extract content
            if "pdf_content" not in st.session_state:
                with st.spinner("Reading document content... This may take a moment."):
                    pdf_content, error = extract_text_from_pdf(uploaded_file)
                    if error:
                        display_error(error)
                    elif pdf_content:
                        st.session_state.pdf_content = pdf_content
                        content_preview(pdf_content)

            # Create enhanced tabs with icons for different functionalities
            tabs = st.tabs(["📄 **Summary**", "🧩 **Interactive Quiz**"])

            # Summary Tab
            with tabs[0]:
                st.markdown("### Document Summary")

                # Add description
                st.markdown(
                    """
                <div style="margin-bottom: 20px;">
                    Generate a comprehensive summary of the document content. This will extract key information,
                    main points, and important details from the PDF to provide a clear overview.
                </div>
                """,
                    unsafe_allow_html=True,
                )

                # Generate Summary button with improved styling
                generate_col1, generate_col2 = st.columns([1, 3])
                with generate_col1:
                    generate_summary_btn = st.button(
                        "🔍 Generate Summary",
                        key="gen_summary",
                        use_container_width=True,
                    )

                if generate_summary_btn or st.session_state.summary_text:
                    # Only process if we don't already have summary data
                    if not st.session_state.summary_text:
                        with st.spinner(
                            "Generating comprehensive document summary... This may take a few minutes."
                        ):
                            summary = generate_summary(st.session_state.pdf_content)
                            st.session_state.summary_text = summary

                    # Display the summary with a nice animation
                    st.markdown(
                        """
                    <style>
                    .summary-container {
                        animation: fadeInUp 0.6s ease-out;
                    }
                    @keyframes fadeInUp {
                        from { opacity: 0; transform: translateY(20px); }
                        to { opacity: 1; transform: translateY(0); }
                    }
                    </style>
                    <div class="summary-container">
                    """,
                        unsafe_allow_html=True,
                    )

                    display_summary(st.session_state.summary_text)

                    st.markdown("</div>", unsafe_allow_html=True)

            # Quiz Tab
            with tabs[1]:
                st.markdown("### Interactive Quiz")

                # Add description
                st.markdown(
                    """
                <div style="margin-bottom: 20px;">
                    Create a multiple-choice quiz based on the document content. Test your understanding
                    of the material with questions generated from the key concepts in the PDF.
                </div>
                """,
                    unsafe_allow_html=True,
                )

                # Generate Quiz button with improved styling
                quiz_col1, quiz_col2 = st.columns([1, 3])
                with quiz_col1:
                    generate_quiz_btn = st.button(
                        "🧩 Generate Quiz", key="gen_quiz", use_container_width=True
                    )

                if generate_quiz_btn or st.session_state.quiz_data:
                    # Only process if we don't already have quiz data
                    if not st.session_state.quiz_data:
                        with st.spinner(
                            "Creating quiz questions... This may take a few minutes."
                        ):
                            st.session_state.quiz_data = generate_quiz(
                                st.session_state.pdf_content
                            )

                            # Reset user answers for the new quiz
                            questions = st.session_state.quiz_data.get("questions", [])
                            st.session_state.user_answers = [""] * len(questions)
                            st.session_state.quiz_submitted = False
                            st.session_state.score = 0

                    # Add animation for quiz display
                    st.markdown(
                        """
                    <style>
                    .quiz-container {
                        animation: fadeInRight 0.6s ease-out;
                    }
                    @keyframes fadeInRight {
                        from { opacity: 0; transform: translateX(20px); }
                        to { opacity: 1; transform: translateX(0); }
                    }
                    </style>
                    <div class="quiz-container">
                    """,
                        unsafe_allow_html=True,
                    )

                    # Display the quiz
                    display_interactive_quiz(st.session_state.quiz_data)

                    st.markdown("</div>", unsafe_allow_html=True)

                # Create new quiz button with improved styling
                if "quiz_data" in st.session_state and st.session_state.quiz_data:
                    if st.button(
                        "🔄 Create New Quiz", key="new_quiz", type="secondary"
                    ):
                        # Clear previous quiz data to force regeneration
                        st.session_state.quiz_data = None
                        st.session_state.quiz_submitted = False
                        st.session_state.user_answers = []  # Reset to empty list first
                        st.session_state.score = 0

                        # Regenerate quiz
                        with st.spinner("Generating new quiz questions..."):
                            st.session_state.quiz_data = generate_quiz(
                                st.session_state.pdf_content
                            )

                            # Initialize user_answers with correct length for new quiz
                            questions = st.session_state.quiz_data.get("questions", [])
                            st.session_state.user_answers = [""] * len(questions)

                            st.rerun()

    # Add footer
    st.markdown(
        """
    <div style="text-align: center; margin-top: 3rem; padding: 1rem; border-top: 1px solid #f0f0f0;">
        <p style="color: #888; font-size: 0.8rem;">
            Quiz & Summary Generator | Built with Streamlit and Ollama
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
