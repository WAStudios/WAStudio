import os
import hashlib

# CHANGE THIS PATH to your icons folder (can be absolute or relative)
icons_folder = r'C:\Users\Jon Skocik\Downloads\icons'  # Adjust as needed
output_filenames_txt = os.path.join(icons_folder, '..', 'filenames.txt')

def generate_filenames_file(folder, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        for root, dirs, files in os.walk(folder):
            for name in sorted(files):  # Sorted for consistent order
                rel_path = os.path.relpath(os.path.join(root, name), folder)
                f.write(rel_path + '\n')
    print(f"Generated {output_file}")

def md5_file(filepath):
    hash_md5 = hashlib.md5()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

# Generate filenames.txt
generate_filenames_file(icons_folder, output_filenames_txt)

# Compute MD5 of filenames.txt
hash_value = md5_file(output_filenames_txt)
print(f"MD5 of filenames.txt: {hash_value}")
