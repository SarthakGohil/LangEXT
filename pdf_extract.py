import langextract as lx
import textwrap
import os
import pdfplumber

if "GEMINI_API_KEY" in os.environ:
    del os.environ["GEMINI_API_KEY"]

os.environ["LANGEXTRACT_API_KEY"] = ""

class GeminiExtractor:
    def __init__(self, prompt, data, examples, model="gemini-2.5-flash"):
        self.prompt = prompt
        self.data = data
        self.examples = examples
        self.model = model
        
    def extraction(self):
        try:
            res = lx.extract(
                text_or_documents=self.data,
                prompt_description=self.prompt,
                examples=self.examples,
                model_id=self.model
            )
            return res
        except Exception as e:
            return f"Error during extraction: {e}"

class PDFParser:
    def __init__(self, pdf_file_path):
        self.pdf_path = pdf_file_path
        self.text_content = self._read_pdf()
    
    def _read_pdf(self):
        if not os.path.exists(self.pdf_path):
            raise FileNotFoundError(f"File not found: {self.pdf_path}")
            
        full_text = ""
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        full_text += page_text + "\n"
        except Exception as e:
            print(f"Error reading PDF: {e}")
            return ""
            
        return full_text

    def extract_info(self):
        # 1. promt for model
        prompt = textwrap.dedent("""\
            Analyze the provided document text and extract structured metadata.
            
            Identify the core subject matter and extraction the following fields:
            - Title: The main heading or title of the document.
            - Date: The primary date associated with the document (publication or event date).
            - Author: The person or organization who wrote it.
            - Summary: A 1-sentence summary of the content.
            
            OUTPUT:
            Highlight the Title as the 'extraction_text'.
            Store 'Date', 'Author', and 'Summary' inside the 'attributes' dictionary.
            """)
        
        # 2. examples
        examples = [
            lx.data.ExampleData(
                text="""
                    Q3 FINANCIAL REPORT
                    Prepared by: Sarah Jenkins
                    Date: October 15, 2025
                    
                    This quarter we saw a 20% increase in user retention across all mobile platforms.
                    Revenue exceeded expectations by $2M.
                """,
                extractions=[
                    lx.data.Extraction(
                        extraction_class="PDF_Metadata",
                        extraction_text="Q3 FINANCIAL REPORT",
                        attributes={
                            "Date": "2025-10-15",
                            "Author": "Sarah Jenkins",
                            "Summary": "Q3 report showing 20% retention growth and revenue exceeding targets."
                        }
                    )
                ] 
            )
        ]
        
        extractor = GeminiExtractor(prompt, self.text_content, examples)
        return extractor.extraction()


pdf_file = "lab3.pdf" 

if os.path.exists(pdf_file):
    try:
        parser = PDFParser(pdf_file)
        
        if parser.text_content:
            if len(parser.text_content) > 30000: 
                parser.text_content = parser.text_content[:30000]
                print("Notice: PDF text truncated to first 30k characters.")

            result = parser.extract_info()
            print(result)

            if hasattr(result, 'extractions') and result.extractions:
                for item in result.extractions:
                    print(f"--- Extracted Document: {item.extraction_text} ---")
                    print(f"Author:  {item.attributes.get('Author', 'N/A')}")
                    print(f"Date:    {item.attributes.get('Date', 'N/A')}")
                    print(f"Summary: {item.attributes.get('Summary', 'N/A')}")
            else:
                print("No information extracted. (Check if PDF text is readable)")
                
    except Exception as e:
        print(f"An error occurred: {e}")

else:     
    print("Sorry, File Not Exist!!!")