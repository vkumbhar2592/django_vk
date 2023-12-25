def add_end_before_executive(file_path):
    # Read the content of the file
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.readlines()
    
    # Add <END>\n before each "Executive:" line, except the first one
    with open(file_path, 'w', encoding='utf-8') as file:
        for line in content:
            if 'Executive:' in line and content.index(line) != 0:
                file.write('<END>\n')
            file.write(line)

# Replace 'path_to_file.txt' with the path to your actual text file
# file_path = "../intial_data_clean/yahooealistapollo.txt"
# add_end_before_executive(file_path)

# file_path = "../intial_data_clean/yahooealistemea.txt"
# add_end_before_executive(file_path)

file_path = "../tmp/yahooealisatapac.txt"
add_end_before_executive(file_path)
