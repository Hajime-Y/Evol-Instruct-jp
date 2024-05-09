import re

# def _extract_next_generation(filename):
#     match = re.search(r'gen(\d+)', filename)
#     if match:
#         current_generation = int(match.group(1))
#         return current_generation + 1
#     else:
#         return 1

# def create_new_generation_filename(filename):
#     """
#     指定されたファイル名から新しい世代のファイル名を生成します。
    
#     Args:
#         filename (str): 元のファイル名。
        
#     Returns:
#         str: 新しい世代のファイル名。
#     """
#     new_generation = _extract_next_generation(filename)
#     base_name, extension = re.match(r"^(.*?)(\.\w+)?$", filename).groups()
#     base_name = re.sub(r'_gen\d+', '', base_name)
#     new_filename = f"{base_name}_gen{new_generation}{extension if extension else ''}"
#     return new_filename

# def create_eliminated_generation_filename(filename):
#     """
#     指定されたファイル名から、削除された世代の新しいファイル名を生成します。
    
#     Args:
#         filename (str): 元のファイル名。
        
#     Returns:
#         str: 削除された世代の新しいファイル名。
#     """
#     new_generation = _extract_next_generation(filename)
#     base_name, extension = re.match(r"^(.*?)(\.\w+)?$", filename).groups()
#     base_name = re.sub(r'_gen\d+', '', base_name)
#     eliminated_filename = f"{base_name}_eliminated_gen{new_generation}{extension if extension else ''}"
#     return eliminated_filename

# def extract_file_details(file_path):
#     """
#     指定されたファイルパスからファイルのフォルダとファイル名を抽出します。

#     Args:
#         file_path (str): ファイルの完全なパス。

#     Returns:
#         tuple: ファイルが存在するフォルダのパスとファイル名を含むタプル。
#     """
#     import os
#     file_folder = os.path.dirname(file_path)
#     filename = os.path.basename(file_path)
#     return file_folder, filename