import os
import re
import json
import dotenv
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
from pathlib import Path
from PyPDF2 import PdfReader

 
dotenv.load_dotenv()

 
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)

def read_prompt(prompt_path: str):
    """Read the prompt for document parsing from a text file."""
    with open(prompt_path, "r", encoding='utf-8') as f:
        return f.read()

def extract_text_from_pdf(pdf_path: str):
    """Extract text content from a PDF file using PyPDF2."""
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"Error extracting text from PDF {pdf_path}: {e}")
        return ""
# HTML Extraction
def extract_text_from_html(html_path: str):
    """Extract text content from an HTML file."""
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
        
        # Extract text, removing scripts, styles, and extra whitespace
        text = ' '.join(soup.stripped_strings)
        return text
    except Exception as e:
        print(f"Error extracting text from HTML {html_path}: {e}")
        return ""

def extract_metadata(content: str, prompt_path: str, model_name: str = 'gemini-pro'):
    """Extract metadata from document content using Gemini model."""
    prompt_data = read_prompt(prompt_path)

    try:
        model = genai.GenerativeModel(model_name)
        
        full_prompt = f"{prompt_data}\n\nDocument Content:\n{content}"
        
        response = model.generate_content(full_prompt)
        response_content = response.text
        
        if not response_content:
            print("Empty response from the model")
            return {}

        # Clean and parse JSON
        response_content = re.sub(r'```json\s*', '', response_content)
        response_content = re.sub(r'\s*```', '', response_content)

        try:
            return json.loads(response_content)
        except json.JSONDecodeError:
            # extract JSON from response
            match = re.search(r'\{.*\}', response_content, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group(0))
                except json.JSONDecodeError:
                    print("Failed to extract valid JSON")
            return {}

    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return {}

def process_document(doc_path: str, prompt_path: str, output_folder: str):
    """Process a single document through the extraction pipeline."""
    print(f"Processing document: {doc_path}")

    try:
        # Determine file type and extract content
        file_ext = os.path.splitext(doc_path)[1].lower()
        
        if file_ext == '.pdf':
            content = extract_text_from_pdf(doc_path)
        elif file_ext in ['.html', '.htm']:
            content = extract_text_from_html(doc_path)
        else:
            print(f"Unsupported file type: {file_ext}")
            return

        if not content:
            print(f"No text extracted from {doc_path}")
            return

        metadata = extract_metadata(content, prompt_path)
        
        if not metadata:
            print(f"Failed to extract metadata for {doc_path}")
            return

        output_filename = Path(doc_path).stem + '.json'
        output_path = os.path.join(output_folder, output_filename)

        os.makedirs(output_folder, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        print(f"Saved metadata to {output_path}")

    except Exception as e:
        print(f"Error processing {doc_path}: {e}")

def process_directory(prompt_path: str, directory_path: str, output_folder: str):
    """Process all supported files in the given directory."""
    for filename in os.listdir(directory_path):
        # Support for both PDF and HTML files
        if filename.lower().endswith(('.pdf', '.html', '.htm')):
            doc_path = os.path.join(directory_path, filename)
            process_document(doc_path, prompt_path, output_folder)

# Execution
if __name__ == "__main__":
    prompt_path = "./data/prompts/document_prompt.txt"
    directory_path = "./data"
    output_folder = "./data/extracted_metadata"

    process_directory(prompt_path, directory_path, output_folder)