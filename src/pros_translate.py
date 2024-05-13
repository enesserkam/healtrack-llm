import fitz  # PyMuPDF
import os
from deep_translator import GoogleTranslator


def translate_text(text, src_lang='tr', dest_lang='en'):
    print("call translate_text")
    try:
        translated_text = GoogleTranslator(source=src_lang, target=dest_lang).translate(text)
        print(translated_text)
        return translated_text
    except Exception as e:
        print(f"Error during translation: {e}")
        return ""


def save_text_to_file(text, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(text)


def process_pdfs(folder_read, folder_write):
    for filename in os.listdir(folder_read):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(folder_read, filename)
            print(pdf_path)
            doc = fitz.open(pdf_path)
            full_translated_text = ''

            for page in doc:
                page_text = page.get_text()
                print("try translate_text")
                translated_text = translate_text(page_text)
                full_translated_text += translated_text

            doc.close()

            if full_translated_text:
                txt_filename = os.path.join(folder_write, f"{os.path.splitext(filename)[0]}_translated.txt")
                save_text_to_file(full_translated_text, txt_filename)
                print(f"Processed and saved: {txt_filename}")


# Usage
if __name__ == '__main__':
    read_folder = 'downloaded_pdfs/'
    write_folder = 'translated_pros/'
    process_pdfs(read_folder, write_folder)
