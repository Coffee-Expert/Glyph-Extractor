# PDF Glyph Extractor



<div align="center">
    <img src="https://img.shields.io/badge/-Python-black?style=for-the-badge&logoColor=white&logo=python&color=3776AB" alt="python" />
    <img src="https://img.shields.io/badge/-PDFMiner-black?style=for-the-badge&logoColor=white&color=FFD43B" alt="pdfminer" />
    <img src="https://img.shields.io/badge/-Tesseract-black?style=for-the-badge&logoColor=white&color=5A5A5A" alt="tesseract" />
    <img src="https://img.shields.io/badge/-Xpdf-black?style=for-the-badge&logoColor=white&color=DD4814" alt="xpdf" />
    <img src="https://img.shields.io/badge/-Pillow-black?style=for-the-badge&logoColor=white&color=37A9CA" alt="pillow" />
    <img src="https://img.shields.io/badge/-BeautifulSoup-black?style=for-the-badge&logoColor=white&color=FFA500" alt="beautifulsoup" />
    <img src="https://img.shields.io/badge/-Poppler-black?style=for-the-badge&logoColor=white&color=FF9900" alt="poppler" />
    <img src="https://img.shields.io/badge/-Pytesseract-black?style=for-the-badge&logoColor=white&color=5F6368" alt="pytesseract" />
</div>



## Author
**Abhishek Kevin Gomes**  
GitHub: [Coffee-Expert](https://github.com/Coffee-Expert)

## Project Overview
The **PDF Glyph Extractor** is a comprehensive tool designed to extract textual and metadata information from PDF documents. This project is useful for tasks such as Optical Character Recognition (OCR), PDF parsing, and detailed document analysis. It provides a robust method for converting PDF content into text, images, and HTML representations while preserving metadata such as glyph codes, font sizes, and positions on the page.

## Tech Stack
- **Python**: The primary programming language used for this project.
- **PDFMiner**: A tool for extracting text, images, and other content from PDF files.
- **Tesseract**: An OCR engine used to extract text from images.
- **Xpdf**: A suite of tools for manipulating PDF files, including metadata extraction.
- **Pillow**: A Python Imaging Library used for image processing.
- **BeautifulSoup**: A library for web scraping, used here for parsing HTML.
- **Poppler**: A PDF rendering library that facilitates the conversion of PDF pages to images.
- **Pytesseract**: A Python wrapper for Tesseract OCR, used for text extraction from images.

## Features
- **Text Extraction from Images**: Utilizes OCR (Optical Character Recognition) to extract text from images generated from PDF pages.
- **Text Extraction with PDFMiner**: Extracts textual content directly from the PDF using the PDFMiner library.
- **Glyph Information Extraction**: Captures detailed glyph information, including Unicode values, font sizes, positions, and more.
- **PDF Metadata Extraction**: Extracts and processes metadata from PDF documents using the xpdf toolset.
- **HTML Representation**: Generates an HTML representation of the PDF document with hoverable glyph information, displaying Unicode values, glyph codes, font sizes, and more.

## Project Working (Step by Step)
### Step 1: Extract Text from Images (OCR)
- Converts PDF pages to images using `pdf2image`.
- Extracts text from these images using the Tesseract OCR engine.

### Step 2: Extract Text with PDFMiner
- Extracts text directly from the PDF using PDFMiner and saves it with metadata.

### Step 3: Extract Glyph Information
- Extracts glyph-level information including Unicode, font size, and position using PDFMiner.

### Step 4: Generate HTML Representation
- Generates an HTML representation of the PDF, overlaying extracted text information on the image of each page. Hovering over text elements reveals glyph information.

### Step 5: Save Outputs
- Saves extracted text, glyph information, and HTML representations to specified output directories.

## Installation
### Prerequisites
- **Python 3.7+**
- **Poppler for Windows**: Required for PDF to image conversion.
- **Tesseract-OCR**: Required for OCR functionality.
- **Xpdf-tools**: Required for extracting PDF metadata.

### Installation Steps
1. Clone the repository:
    ```bash
    git clone https://github.com/Coffee-Expert/Glyph-Extractor
    cd PDF-Glyph-Extractor
    ```
2. Install required Python packages:
    ```bash
    pip install -r requirements.txt
    ```
3. Install **Poppler** and **Tesseract-OCR**:
    - Download and install [Poppler for Windows](http://blog.alivate.com.au/poppler-windows/).
    - Download and install [Tesseract-OCR](https://github.com/tesseract-ocr/tesseract).

4. Set the paths in the script:
    - Update the paths for `poppler_path`, `tesseract_path`, and `pdftohtml_path` in the script to match your installation.

## Usage
1. Place your PDF file in the `pdfs/` directory.
2. Run the main script:
    ```bash
    python main.py
    ```
3. The script will output the extracted text, glyph information, and HTML representation to the `output/` directory.

## Screenshots
### 1. Project Code with Steps
![ss code](https://github.com/user-attachments/assets/d80eb57d-dea9-4a75-9d72-359162b9102e)


### 2. Glyph & Unicode Information
![ss code 2](https://github.com/user-attachments/assets/d2e98312-89f1-4f94-8a94-5c0974ad61f5)


### 3. HTML Representation
![html rep 2](https://github.com/user-attachments/assets/6720b9fb-2597-47c7-b3a3-eb0b7ed8e0f1)
![ss rep 2](https://github.com/user-attachments/assets/870c2b7f-809f-4db2-93dc-f6d496802122)
![ss rep](https://github.com/user-attachments/assets/1e4a8ce8-7ba7-479b-bea0-5568f046c3f5)
![html rep](https://github.com/user-attachments/assets/db8fe808-e6a7-4786-9e40-c49bdbdb2f53)



## Contributions
Contributions to this project are welcome! Feel free to open an issue or submit a pull request on GitHub. Please follow the contribution guidelines when submitting new features or bug fixes.

