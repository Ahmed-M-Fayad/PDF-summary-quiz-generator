# PDF Quiz & Summary Generator - NTI Graduation Project

This project is a graduation project for the **National Telecommunication Institute (NTI) - Huawei Egyptian Talents Academy (ETA)** Artificial Intelligence course. Developed over **80 hours**, this Streamlit-based web application processes PDF files to generate detailed summaries and interactive multiple-choice quizzes using the Ollama API (`llama3:latest`).

## Project Overview

The PDF Quiz & Summary Generator allows users to upload PDF documents and automatically generate:
* **Detailed Summaries**: Concise summaries of the PDF content
* **Interactive Quizzes**: Multiple-choice questions with explanations based on document content

The application features a responsive UI with light/dark mode support and performance optimizations for efficient processing.

## Contributors

This project was developed under the guidance of:
- **Eng. Ahmed Ali** (Mentor)

Project Engineers:
- Eng. Ahmed M. Fayad
- Eng. Mohammad Abdelhay
- Eng. Youssef Bedeir
- Eng. Ahmed Ammar
- Eng. Amr Elnashar

## Features

* **PDF Processing**: Extracts text from uploaded documents efficiently
* **Summary Generation**: Creates detailed summaries from PDF content
* **Quiz Generation**: Produces interactive quizzes with multiple-choice questions
* **Responsive Design**: Supports various screen sizes with light/dark themes
* **Performance Optimized**: Includes caching and input truncation for faster processing

## Installation

1. **Clone the Repository**

```bash
git clone https://github.com/Ahmed-M-Fayad/PDF-summary-quiz-generator.git
cd PDF-summary-quiz-generator
```

2. **Install Python Dependencies**

```bash
pip install -r requirements.txt
```

Requirements include streamlit, PyPDF2, requests, and python-dotenv.

3. **Install and Configure Ollama**
   * Download from https://ollama.com/
   * Pull the model: `ollama pull llama3:latest`
   * Start the server: `ollama serve`

## Usage

1. **Run the Streamlit App**

```bash
streamlit run app.py
```

2. **Access the Application** Open your browser to `http://localhost:8501`

3. **Upload a PDF** Use the file uploader on the homepage to select a PDF document

4. **Generate Content**
   * Navigate to the Summary tab and click "Generate Summary"
   * Navigate to the Quiz tab and click "Generate Quiz"
   * Interact with the generated quiz by selecting answers and viewing explanations

Note: Ensure the Ollama server is running during application use.

## About the NTI-Huawei ETA Course

The Artificial Intelligence course offered by NTI in collaboration with Huawei developed my skills in:
* Python programming for AI development
* Data analysis techniques and machine learning
* Deep learning models and AI frameworks
* Huawei AI platforms and applications

This 80-hour intensive training provided hands-on experience with modern AI concepts and techniques, culminating in this graduation project that demonstrates practical application of these skills.

## License

This project is licensed under the MIT License.

## Acknowledgments

* National Telecommunication Institute (NTI) for hosting the program
* Huawei Egyptian Talents Academy (ETA) for educational resources
* Ollama and Streamlit for their development frameworks
