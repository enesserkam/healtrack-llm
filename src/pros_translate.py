import os
import concurrent.futures
from deep_translator import GoogleTranslator

def split_text_into_chunks(text, max_length=4500):
    """Split the text into fixed-size chunks of max_length characters."""
    return [text[i:i + max_length] for i in range(0, len(text), max_length)]

def process_file(file_path, src_folder, dest_folder):
    """ Process each file: translate in fixed-size batches and write. """
    dest_subfolder = os.path.splitext(file_path.replace(src_folder, dest_folder))[0] + '_translated.txt'
    os.makedirs(os.path.dirname(dest_subfolder), exist_ok=True)

    translator = GoogleTranslator(source='tr', target='en')

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()

        chunks = split_text_into_chunks(text)
        translated_text = ""

        for chunk in chunks:
            translated_chunk = translator.translate(chunk)
            translated_text += translated_chunk

        with open(dest_subfolder, 'w', encoding='utf-8') as f:
            f.write(translated_text.strip())

        print(f"Processed and saved: {dest_subfolder}")

    except Exception as e:
        print(f"Error during translation of {file_path}: {e}")

def process_subfolder(subfolder, src_folder, dest_folder):
    """ Process each text file in the subfolder. """
    for filename in os.listdir(subfolder):
        file_path = os.path.join(subfolder, filename)
        if filename.endswith('.txt'):
            process_file(file_path, src_folder, dest_folder)

def main():
    src_folder = 'pdf_subfolders'
    dest_folder = 'translated_pros'
    os.makedirs(dest_folder, exist_ok=True)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        subfolders = [os.path.join(src_folder, f) for f in os.listdir(src_folder) if os.path.isdir(os.path.join(src_folder, f))]
        executor.map(process_subfolder, subfolders, [src_folder]*len(subfolders), [dest_folder]*len(subfolders))


if __name__ == '__main__':
    main()
