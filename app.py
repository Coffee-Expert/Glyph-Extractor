import os
import io
import fitz  
import hashlib
import subprocess
import pytesseract
from PIL import Image
from bs4 import BeautifulSoup
from pdf2image import convert_from_path
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextBoxHorizontal, LTChar, LTTextLineHorizontal


#Path Definition
pdf_path = 'pdfs/document.pdf'
images_path = 'images/'
output_text_path = 'output/output_text.txt'
output_html_path = 'output/output_text.html'
unicode_info_path = 'output/unicode_characters.txt'
poppler_path = r'poppler\bin'
tesseract_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
pdftohtml_path = r'C:\Users\Administrator\Desktop\shwarma ai\xpdf-tools-win-4.05\bin64\pdftohtml.exe'

#Directory Creation
os.makedirs(images_path, exist_ok=True)
os.makedirs(os.path.dirname(output_text_path), exist_ok=True)
os.makedirs(os.path.dirname(output_html_path), exist_ok=True)
os.makedirs(os.path.dirname(unicode_info_path), exist_ok=True)


#Define Helper Functions

def generate_glyph_code(unicode_val, x, y, page_num):
    
    #Generate a unique glyph code based on Unicode value, position, and page number.
    glyph_string = f"{unicode_val}-{x}-{y}-{page_num}"
    
    # Generate an MD5 hash of the string to create a unique glyph code
    glyph_code = hashlib.md5(glyph_string.encode()).hexdigest()
    
    return glyph_code

def extract_text_from_images(images_path):
   
    # Extract text from images using OCR (pytesseract).
    print(" Extracting text from images (OCR)...")
    extracted_text = ""
    for image_file in os.listdir(images_path):
        if image_file.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
            image_path = os.path.join(images_path, image_file)
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image, lang='eng', config='--psm 6')
            extracted_text += text + "\n"
            print(f'Extracted text from {image_file}')
    return extracted_text

def extract_text_with_pdfminer(pdf_path):

    #Extract Text
    print(" Extracting text with PDFMiner...")
    output = io.StringIO()
    with open(pdf_path, 'rb') as f:
        for page_layout in extract_pages(f):
            for element in page_layout:
                if isinstance(element, LTTextBoxHorizontal):
                    for text_line in element:
                        if isinstance(text_line, LTTextLineHorizontal):
                            output.write(text_line.get_text())
    return output.getvalue()

def save_text_with_metadata(text, output_path):
    
    print(f"Saving extracted text with metadata to {output_path}...")
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(text)
    print("Text with metadata saved successfully!")

def extract_pdf_metadata_with_xpdf(pdf_path):
    #Extract PDF Metadata if present
    print(" Extracting PDF metadata with xpdf's pdftohtml...")
    html_dir = 'output'
    html_path = os.path.join(html_dir, 'document.html')

     
    if os.path.exists(html_dir):
        print(f"Output directory '{html_dir}' already exists. Removing its contents...")
        for root, dirs, files in os.walk(html_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
    
    # Create the output directory
    os.makedirs(html_dir, exist_ok=True)

    # Command to convert PDF to HTML with metadata
    cmd = [
        pdftohtml_path, 
        '-meta',       
        '-noframes',   
        '-c',           
        '-hidden',      
        '-xml',         
        pdf_path, 
        html_dir
    ]
    
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing pdftohtml: {e}")
        return []

    # Parse HTML file for text and metadata
    metadata = []
    if os.path.exists(html_path):
        with open(html_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')
            
            for text in soup.find_all('text'):
                x = text.get('x', '0')
                y = text.get('y', '0')
                content = text.get_text(strip=True)
                font = text.get('font', 'unknown')
                size = text.get('size', 'unknown')
                bbox = text.get('bbox', '0 0 0 0').split()
                
                metadata.append({
                    "text": content,
                    "font": font,
                    "size": size,
                    "bbox": bbox,
                    "x": float(x),
                    "y": float(y),
                })
    else:
        print(f"HTML file not found: {html_path}")

    return metadata

def extract_glyph_info(pdf_path):
    """
    Extract glyph information from PDF using PDFMiner.
    """
    print(" Extracting glyph information...")
    glyphs = []
    for page_num, page_layout in enumerate(extract_pages(pdf_path)):
        for element in page_layout:
            if isinstance(element, LTTextBoxHorizontal):
                for text_line in element:
                    if isinstance(text_line, LTTextLineHorizontal):
                        for char in text_line:
                            if isinstance(char, LTChar):
                                text = char.get_text()
                                if text:  # Ensure text is not empty
                                    for single_char in text:  # Iterate over each character in the text
                                        unicode_val = ord(single_char)
                                        glyph_code = generate_glyph_code(unicode_val, char.x0, char.y0, page_num)
                                        glyphs.append({
                                            "glyph_code": glyph_code,
                                            "text": single_char,
                                            "unicode": unicode_val,
                                            "font_size": char.size,
                                            "x": char.x0,
                                            "y": char.y0,
                                            "page_num": page_num
                                        })
    print(f"Total glyphs extracted: {len(glyphs)}")
    return glyphs


def convert_pdf_to_images(pdf_path, images_path, poppler_path):
     
   
   # Convert PDF pages to images using pdf2image.
    print("Converting PDF pages to images...")
    images = convert_from_path(pdf_path, poppler_path=poppler_path)
    image_paths = []
    for i, image in enumerate(images):
        image_path = os.path.join(images_path, f'page_{i + 1}.png')
        image.save(image_path, 'PNG')
        image_paths.append(image_path)
        print(f'Saved image: {image_path}')
    return image_paths

def generate_html_representation(pdf_path, images_path, output_html_path, glyphs):
    
    """
    Generate an HTML representation of the PDF with hover information displaying glyph codes.
    """
    print(" Generating HTML representation...")
    image_paths = convert_pdf_to_images(pdf_path, images_path, poppler_path)

     
    doc = fitz.open(pdf_path)

    # Start building the HTML content
    html_content = (
        '<!DOCTYPE html>'
        '<html>'
        '<head>'
        '<meta charset="UTF-8">'
        '<title>PDF HTML Representation</title>'
        '<style>'
        'body { font-family: Arial, sans-serif; margin: 0; padding: 0; }'
        '.container { position: relative; width: 100%; height: auto; overflow: hidden; margin-bottom: 20px; }'
        '.text-box { position: absolute; border: 1px solid red; padding: 2px; font-size: 12px;'
        'background: transparent; z-index: 1000; }'
        '.text-box:hover .info { display: block; }'
        '.info { display: none; background: rgba(0, 0, 0, 0.7); color: #fff; padding: 5px; border-radius: 3px;'
        'position: absolute; top: 100%; left: 0; white-space: nowrap; z-index: 1001; }'
        '</style>'
        '</head>'
        '<body>'
    )

    for page_num, image_path in enumerate(image_paths):
        page = doc.load_page(page_num)
        page_width, page_height = page.rect.width, page.rect.height

        image_name = os.path.basename(image_path)
        html_content += (
            f'<div class="container" style="width: {page_width +1}px; height: {page_height +1}px;">'
            f'<img src="../{image_path}" style="position: absolute; left: 0; top: 0; width: {page_width}px; height: {page_height}px; border: 1px solid black" />'
        )

         
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        bbox = span["bbox"]
                        text = span["text"]
                        font = span["font"]
                        size = span["size"]
                        left, top, right, bottom = bbox
                        width = right - left
                        height = bottom - top

                        # Generate glyph code for each span based on its text and position
                       
                        if text:
                            unicode_val = ord(text[0])  # Using the first character for demonstration
                            glyph_code = generate_glyph_code(unicode_val, left, top, page_num)
                        else:
                            glyph_code = "N/A"

                        
                        info_content = (
                            f'<strong>Text:</strong> {text}<br>'
                            f'<strong>Unicode:</strong> {", ".join(f"U+{ord(c):04X}" for c in text)}<br>'
                            f'<strong>Glyph Code:</strong> {glyph_code}<br>'
                            f'<strong>Font:</strong> {font}<br>'
                            f'<strong>Size:</strong> {size}<br>'
                            f'<strong>Width:</strong> {width:.2f}px<br>'
                            f'<strong>Height:</strong> {height:.2f}px<br>'
                            f'<strong>Position:</strong> Left: {left:.2f}px, Top: {top:.2f}px, '
                            f'Right: {right:.2f}px, Bottom: {bottom:.2f}px<br>'
                        )

                      
                        html_content += (
                            f'<div class="text-box" style="left: {left}px; top: {top}px; width: {width}px; '
                            f'height: {height}px; font-size: {size}px;">'
                            f'<span class="info">{info_content}</span>'
                            f'</div>'
                        )

        html_content += '</div>'   

    html_content += '</body></html>'

     
    with open(output_html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"HTML representation saved to {output_html_path}")

# =======================
# Step 0: Main Function
# =======================
def main():
    """
    Main function to orchestrate the PDF processing steps.
    """
    # -------------------
    # Step 1: Extract Text from Images (OCR)
    # -------------------
    image_text = extract_text_from_images(images_path)
    print(f"Extracted text from images (snippet): {image_text[:100]}...")  # Print a snippet

    # -------------------
    # Step 2: Extract Text with PDFMiner
    # -------------------
    pdfminer_text = extract_text_with_pdfminer(pdf_path)
    save_text_with_metadata(pdfminer_text, output_text_path)

    # -------------------
    # Step 3: Extract Glyph Information
    # -------------------
    glyph_info = extract_glyph_info(pdf_path)

    # -------------------
    # Step 4: Save Glyph Information
    # -------------------
    with open(unicode_info_path, 'w', encoding='utf-8') as file:
        for glyph in glyph_info:
            file.write(
                f"Glyph Code: {glyph['glyph_code']}, "
                f"Text: {glyph['text']}, "
                f"Unicode: {glyph['unicode']}, "
                f"Font Size: {glyph['font_size']}, "
                f"Position: ({glyph['x']}, {glyph['y']}), "
                f"Page: {glyph['page_num']}\n"
            )
    print(f"Glyph information saved to {unicode_info_path}")

    # -------------------
    # Step 5: Generate HTML Representation
    # -------------------
    generate_html_representation(pdf_path, images_path, output_html_path, glyph_info)

# =======================
# Step 6: Execute Main Function
# =======================
if __name__ == "__main__":
    main()
