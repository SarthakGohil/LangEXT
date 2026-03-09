# LangEXT (rag/LangEXT)

Small Python scripts for **information extraction** using LangExtract + LLM APIs.

## Setup

From repo root:

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r rag/requirements.txt
pip install langextract pdfplumber openai google-genai python-dotenv
```

Add keys in `.env` (don’t commit it):

```env
LANGEXTRACT_API_KEY=...
GEMINI_API_KEY=...
OPENAI_API_KEY=...
HF_TOKEN=...
```

## Run

```bash
# PDF -> extract title/date/author/summary (edit pdf path inside script if needed)
python rag/LangEXT/pdf_extract.py

# Generate example training data for LangExtract (uses 1.txt and Gemini API)
python rag/LangEXT/example_extracter.py

# Text file demo (reads rag/LangEXT/1.txt)
python rag/LangEXT/txt_extract.py

# Code classification demo
python rag/LangEXT/LE_1.py
```
