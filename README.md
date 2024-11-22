# Emplay Assignment

This Python script processes documents (PDF and HTML) to extract text and generate metadata using the Google's Gemini API. It is designed to handle structured metadata extraction using a user-defined prompt.

---

## Schematic Diagram

![Pipeline](/emplay.png)

---

## Folder Structure

```bash
emplay_assignment/
├── data/
│   ├── prompts/
│   │   └── document_prompt.txt     
│   ├── sample.pdf                 
│   └── extracted_metadata/        
├── emplay.py                         
├── README.md                                  
└── .env                           
```
---

## Features
- **Text Extraction:** Extract text content from PDFs and HTML documents.
- **Metadata Extraction:** Use Gemini API to generate metadata based on the extracted text.
- **Supports Multiple File Types:** Compatible with `.pdf`, `.html`files.
- **Batch Processing:** Process all supported documents in a directory.
- **JSON Output:** Save extracted metadata as structured JSON files.

---

## Prerequisites

1. **Python**: Install Python 3.8 or higher.
2. **Dependencies**: Install required libraries using `pip3`.
  ```bash
  pip3 install requests
pip3 install PyPDF2
pip3 install beautifulsoup4
pip3 install dotenv
pip3 install google-generativeai
  ```
3. **Gemini API Key**: Obtain your API key from the [Gemini Developer Portal](https://aistudio.google.com/).


---

## How to Run

 
1. Prepare Documents: Place your .pdf, .html, or .htm files in the ./data directory and add the Gemini API to the `.env` file.

2. Run the Script:

``` bash
 python3 main.py
```
3. Output:

 Metadata will be saved as .json files in the ./data/extracted_metadata directory.
 


 