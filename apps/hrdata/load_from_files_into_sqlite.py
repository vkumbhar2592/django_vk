import os
from django.db import models
from .models import Topic, Tag, Document, Region

def load_and_insert_documents(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory, filename)

            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

                # Extract parts of the file
                source = extract_line_after(content, 'Source:')
                title = extract_line_after(content, 'Title:')
                document_content = content.split('Document:\n\n', 1)[1] if 'Document:\n\n' in content else ''

                # Create and save the Document object
                Document.objects.create(name=title, street_url=source, content=document_content)
                print(f"Document {title} saved successfully.")

def extract_line_after(text, keyword):
    try:
        return text.split(keyword, 1)[1].split('\n', 1)[0].strip()
    except IndexError:
        return ''


directory = '/path/to/initial_data_clean'
load_and_insert_documents(directory)