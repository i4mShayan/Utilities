import os
import shutil
import re

EXPORT_FILE_TYPE = ".pdf"
exported_pdfs = 0
groups = 0

def export_pdfs_recursively(root_dir):
    folder_list = list(filter(lambda folder: os.path.isdir(os.path.join(root_dir, folder)), os.listdir(root_dir)))

    if len(folder_list) == 0:
        return

    for folder in folder_list:
        full_folder_path = os.path.join(root_dir, folder)
        for file in os.listdir(full_folder_path):
            if file.endswith(EXPORT_FILE_TYPE):
                original_file_path = os.path.join(full_folder_path, file)
                new_file_path = os.path.join(os.path.dirname(__file__), refined_file_name(full_folder_path, file))
                os.rename(original_file_path, new_file_path)
            if os.path.isdir(full_folder_path):
                export_pdfs_recursively(full_folder_path)
        shutil.rmtree(os.path.join(root_dir, folder))


def refined_file_name(full_folder_path, renaming_file):
    file_name, file_extension = os.path.splitext(renaming_file)
    
    for file in os.listdir(full_folder_path):
        if file == 'result.txt':
            with open(os.path.join(full_folder_path, 'result.txt'), 'r', encoding='utf-8') as result_file:
                file_data = result_file.read()

            identity = identity_match.group(1) if (identity_match := re.search(r'identity:\s*(\d+)\n', file_data)) else ''
            username = username_match.group(1) if (username_match := re.search(r'username:\s*([\S]+)\n', file_data)) else ''
            full_name = full_name_match.group(1) if (full_name_match := re.search(r'full name:\s*([\w\s]+)\n', file_data)) else ''

            return f"{identity}-{full_name}{file_extension}" if full_name not in ('', ' ') else f"{identity}-{username}{file_extension}"

    return file


if __name__ == '__main__':
    root_dir = os.path.dirname(__file__)

    export_pdfs_recursively(root_dir)
    
    for file in os.listdir(root_dir):
        file_name, file_extension = os.path.splitext(file)

        if file_extension == EXPORT_FILE_TYPE:
            index = file_name.find("_", file_name.find("_", file_name.find("_") + 1) + 1)
            if(index != -1 and "-----" in file_name):
                file_name = file_name[index + 1:]
                os.rename(file, file_name + file_extension)

    for file in os.listdir(root_dir):
        file_name, file_extension = os.path.splitext(file)
        
        if file_extension == EXPORT_FILE_TYPE:
            original_file_path = os.path.join(root_dir, file)
            if(exported_pdfs == 0):
                groups += 1
            dest_folder = os.path.join(os.path.dirname(__file__), f"G{groups}")
            new_file_path = os.path.join(dest_folder, file)

            if not os.path.exists(dest_folder):
                os.makedirs(dest_folder)

            os.rename(original_file_path, new_file_path)
            exported_pdfs = (exported_pdfs+1)%10

    
