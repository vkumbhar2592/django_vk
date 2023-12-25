import os
import re
import glob

def replace_src_in_html(file_path):
    # Define the pattern to search for and the replacement string
    pattern = r'src="\.\./\.\./assets/(.*?\.png)"'
    replacement = r'src="{% static \'\1\' %}"'

    # Read the original HTML file
    with open(file_path, 'r', encoding='utf-8') as file:
        file_contents = file.read()

    # Replace occurrences
    updated_contents = re.sub(pattern, replacement, file_contents)

    # Write the updated content back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(updated_contents)

 

# Replace with the path to your assets directory
file_path = 'landing-page.html'
replace_src_in_html(file_path)
