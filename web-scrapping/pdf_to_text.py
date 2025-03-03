import os
import pdfplumber
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to extract text from a single PDF
def extract_text_from_pdf(pdf_path):
    try:
        text = ''
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
        return text
    except Exception as e:
        logging.error(f"Failed to extract text from {pdf_path}: {e}")
        return None

# Function to create a folder and save extracted text
def save_text_to_folder(pdf_path, text, base_folder):
    try:
        pdf_name = os.path.basename(pdf_path).replace('.pdf', '')
        text_folder = os.path.join(base_folder, pdf_name)
        os.makedirs(text_folder, exist_ok=True)

        text_file_path = os.path.join(text_folder, 'extracted_text.txt')
        with open(text_file_path, 'w', encoding='utf-8') as text_file:
            text_file.write(text)
        logging.info(f"Text saved for {pdf_path} in {text_file_path}")
    except Exception as e:
        logging.error(f"Failed to save text for {pdf_path}: {e}")

# Main script to process all PDFs in the nested folders
def main():
    pdf_base_folder = 'ndss'
    text_base_folder = 'extracted_texts_ndss'
    os.makedirs(text_base_folder, exist_ok=True)

    # Walk through all the subdirectories in the base folder
    for root, dirs, files in os.walk(pdf_base_folder):
        if 'data' in dirs:
            data_folder = os.path.join(root, 'data')
            pdf_files = [f for f in os.listdir(data_folder) if f.endswith('.pdf')]

            year_folder_name = os.path.basename(root)
            year_text_folder = os.path.join(text_base_folder, year_folder_name)
            os.makedirs(year_text_folder, exist_ok=True)

            total_files = len(pdf_files)
            for idx, pdf_file in enumerate(pdf_files):
                pdf_path = os.path.join(data_folder, pdf_file)
                logging.info(f"Processing {pdf_path} ({idx + 1}/{total_files})...")

                pdf_text = extract_text_from_pdf(pdf_path)
                if pdf_text:
                    save_text_to_folder(pdf_path, pdf_text, year_text_folder)
                else:
                    logging.warning(f"No text extracted from {pdf_path}.")

    logging.info(f"Text extraction complete. Check folders in '{text_base_folder}'.")

if __name__ == '__main__':
    main()
