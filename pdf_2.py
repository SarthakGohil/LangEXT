import os
import json
import textwrap
import pdfplumber
import google.generativeai as genai

# --- CONFIGURATION ---
# Replace with your actual API Key
os.environ["GOOGLE_API_KEY"] = ""
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

class UniversalPDFParser:
    def __init__(self, pdf_file_path):
        self.pdf_path = pdf_file_path
        self.text_content = self._read_pdf()
    
    def _read_pdf(self):
        """Reads PDF text safely."""
        if not os.path.exists(self.pdf_path):
            print(f"Error: File {self.pdf_path} not found.")
            return None
            
        full_text = ""
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        full_text += text + "\n"
        except Exception as e:
            print(f"Error reading PDF: {e}")
            return None
        return full_text

    def extract_data(self):
        if not self.text_content:
            return {"Error": "No text found in PDF"}

        # Use the standard, stable model
        model = genai.GenerativeModel('gemini-1.5-flash')

        # Universal Prompt: Handles both simple lists and complex scenarios
        prompt = textwrap.dedent(f"""\
            You are a helpful assistant that extracts lab assignment details.
            
            Analyze the text below and extract a JSON object with these fields:
            1. "Lab_Title": (e.g., "Lab Assignment 2", "Lab-3")
            2. "Institution": (e.g., "SVNIT, Surat" or N/A)
            3. "Tasks": A list of tasks found in the document. 
               - If it's a simple list (like Lab 2), just copy the question.
               - If it has scenarios (like Lab 3), include the "Scenario Name" and a "Description".

            DOCUMENT TEXT:
            {self.text_content[:30000]} 

            OUTPUT FORMAT:
            Return ONLY valid JSON. No Markdown formatting.
        """)

        try:
            response = model.generate_content(prompt)
            
            # Clean the response to ensure it parses as JSON
            clean_json = response.text.replace("```json", "").replace("```", "").strip()
            return json.loads(clean_json)
            
        except Exception as e:
            return {"Error": f"AI Parsing Failed: {str(e)}"}

# --- TEST ON LAB 3 (The one that was failing) ---
file_name = "lab3.pdf"  # Change this to "lab2.pdf" to test the other one

print(f"Processing {file_name}...")
parser = UniversalPDFParser(file_name)

if parser.text_content:
    data = parser.extract_data()
    print("\n--- EXTRACTED DATA ---")
    print(json.dumps(data, indent=4))
else:
    print("Could not read file.")