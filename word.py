import os
import dotenv
from PyPDF2 import PdfReader
from docx import Document
from pathlib import Path


dotenv.load_dotenv()

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

def save_text_to_word(text: str, output_path: str):
    """Save extracted text to a Word document."""
    try:
        doc = Document()
       
        for line in text.splitlines():
            doc.add_paragraph(line)
        
      
        doc.save(output_path)
        print(f"Saved Word document to {output_path}")
    except Exception as e:
        print(f"Error saving text to Word file {output_path}: {e}")

def process_document(doc_path: str, output_folder: str):
    """Process a single document (PDF to Word conversion)."""
    print(f"Processing document: {doc_path}")

    try:
      
        content = extract_text_from_pdf(doc_path)

        if not content:
            print(f"No text extracted from {doc_path}")
            return
 
        output_filename = Path(doc_path).stem + '.docx'
        output_path = os.path.join(output_folder, output_filename)

     
        os.makedirs(output_folder, exist_ok=True)
        save_text_to_word(content, output_path)

    except Exception as e:
        print(f"Error processing {doc_path}: {e}")

def process_directory(directory_path: str, output_folder: str):
    """Process all PDF files in the given directory."""
    for filename in os.listdir(directory_path):
        if filename.lower().endswith('.pdf'):
            doc_path = os.path.join(directory_path, filename)
            process_document(doc_path, output_folder)

# Execution
if __name__ == "__main__":
    directory_path = "./data"  
    output_folder = "./data/word_files" 

    process_directory(directory_path, output_folder)
