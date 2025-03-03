import os
import re
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to add spaces between words in dense text
def add_spaces_to_dense_text(text):
    corrected_text = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', text)  # Add space between a lowercase letter and an uppercase letter
    corrected_text = re.sub(r'(?<=[0-9])(?=[A-Za-z])|(?<=[A-Za-z])(?=[0-9])', ' ', corrected_text)  # Add space between letters and digits
    corrected_text = re.sub(r'(?<=[A-Za-z])(?=[A-Za-z][A-Za-z])', ' ', corrected_text)  # Add space in between words that are joined
    return corrected_text

# Function to save corrected text to a folder
def save_corrected_text_to_folder(folder_path, text, base_folder):
    try:
        text_folder = os.path.join(base_folder, folder_path)
        os.makedirs(text_folder, exist_ok=True)

        text_file_path = os.path.join(text_folder, 'corrected_text.txt')
        with open(text_file_path, 'w', encoding='utf-8') as text_file:
            text_file.write(text)
        logging.info(f"Corrected text saved for {folder_path} in {text_file_path}")
    except Exception as e:
        logging.error(f"Failed to save corrected text for {folder_path}: {e}")

# Main script to process all text files and correct spacing
def main():
    extracted_text_base_folder = 'extracted_texts_ndss'
    corrected_text_base_folder = 'corrected_texts_ndss'
    
    os.makedirs(corrected_text_base_folder, exist_ok=True)

    # Walk through all the subdirectories in the extracted text base folder
    for root, dirs, files in os.walk(extracted_text_base_folder):
        for dir_name in dirs:
            year_folder = os.path.join(root, dir_name)
            for subroot, subdirs, subfiles in os.walk(year_folder):
                for subdir in subdirs:
                    text_folder = os.path.join(subroot, subdir)
                    text_file_path = os.path.join(text_folder, 'extracted_text.txt')
                    
                    if os.path.isfile(text_file_path):
                        logging.info(f"Processing {text_file_path}...")
                        
                        with open(text_file_path, 'r', encoding='utf-8') as file:
                            text = file.read()
                        
                        corrected_text = add_spaces_to_dense_text(text)
                        save_corrected_text_to_folder(os.path.relpath(text_folder, extracted_text_base_folder), corrected_text, corrected_text_base_folder)
                    else:
                        logging.warning(f"No text file found in {text_folder}.")

    logging.info(f"Text correction complete. Check folders in '{corrected_text_base_folder}'.")

if __name__ == '__main__':
    main()
