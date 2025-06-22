# PDF Data Extractor and Summarizer

This project extracts data from Form ADT-1 PDF files and generates an AI summary using LangChain.

## Prerequisites

- Python 3.8+
- PDF file named "Form ADT-1-29092023_signed.pdf" in the project directory
- Groq API key (for AI summarization)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd home_assignment
```



2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file with your Groq API key:
```
GROQ_API_KEY=your_api_key_here
```

## Usage

1. Place your Form ADT-1 PDF file in the project directory as "Form ADT-1-29092023_signed.pdf"

2. Run the data extraction:
```bash
python extractor.py
```
This will create:
- `extracted_text.txt`: Raw text from PDF
- `output.json`: Structured data extracted from the PDF

3. Generate AI summary:
```bash
python llm_model.py
```
This will create:
- `summary.txt`: AI-generated summary of the form data



## File Structure

```
home_assignment/
├── extractor.py          # PDF data extraction script
├── llm_model.py           # AI summarization script
├── requirements.txt      # Project dependencies
├── .env                 # Environment variables
└── README.md            # This documentation
```
