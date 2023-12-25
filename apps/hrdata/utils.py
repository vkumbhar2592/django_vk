from django.conf import settings
import getpass
import os
from langchain.document_loaders import DirectoryLoader 
from langchain.text_splitter import CharacterTextSplitter,RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS

from .models import Document

def get_full_docs_after_faiss(query, k=6): 
    # serializer_class = DocumentSerializer 
        result = [] 
        faiss_results = get_faiss_chunks(query)
        # Extract unique IDs from the metadata
        document_ids = {doc[0].metadata['id'] for doc in faiss_results}
        # Fetch documents from the database based on these IDs
        queryset = Document.objects.all()
        queryset = queryset.filter(id__in=document_ids) 
        for doc in queryset:
            result.append(doc) 
 
        return  result

def get_faiss_chunks(query, k=6):
    # Define model and encoding parameters
    embeddings = OpenAIEmbeddings()

    #Having Yahoo in the Query lowers the quality of the results since it is a common word
    query = query.replace("Yahoo", " ").replace("yahoo", " ") 

    db = FAISS.load_local(settings.FAISS_DB, embeddings)
    docs = db.similarity_search_with_score(query,k=k)
    for doc, score in docs:
        print("#"*100)
        print(f"Content: {doc.page_content}, Metadata: {doc.metadata}, Score: {score}")
    return docs

class RecursiveCharacterTextSplitter:
    def __init__(self, chunk_size, length_function=len, separators=None):
        self.chunk_size = chunk_size
        self.length_function = length_function
        self.separators = separators if separators is not None else [' ', '\n', '.']

    def split(self, text):
        chunks = []
        while text:
            # If remaining text is smaller than chunk size, add it to chunks and break
            if self.length_function(text) <= self.chunk_size:
                chunks.append(text)
                break

            split_index = self._find_split_index(text)

            # Add the chunk to the list and remove it from the text
            chunks.append(text[:split_index].strip())
            text = text[split_index:].strip()

        return chunks

    def _find_split_index(self, text):
        # Check for each separator within the chunk size limit
        for sep in self.separators:
            index = text.find(sep, 0, self.chunk_size)
            if index != -1:
                return index + len(sep)

        # If no separator is found, split at chunk size
        return self.chunk_size
    

def find_text_window(query, context_text, window_size, delimiters):

# Example usage
# context = '''
# BONUS PLAN MECHANICS

# Q: Which job levels qualify for this plan and what are the bonus targets for each?
# A: The bonus target is a percentage of the base salary for each eligible level as follows:

# In the job category of E1, the title is "VP" and has a bonus target of 35%. For M6 / IC7, the title is "Senior Director" with a bonus target of 30%. M5 / IC6 corresponds to the title "Director" and carries a bonus target of 25%. The title "Senior Manager" is associated with M4 / IC5 and has a bonus target of 15%. Both M3 / IC4, with the title "Manager", and M2 / IC3, with the title "Assoc Manager / Career Professional", have a bonus target of 15%. IC2 is designated as "Developing Professional" with a bonus target of 10%. IC1, referred to as "Entry Professional", has a bonus target of 5%. Lastly, the categories S1 through S4 are collectively labeled as "Support" and each have a bonus target of 5%.

# *SVP and above targets are undisclosed.
# Refer here for your job level.

# Q: How is my bonus target amount calculated?
# A: Annual Base Salary x Bonus Target Percentage: ($100 x 10% = $10)
# Annual Salary = Annual Base Pay (based on regular hourly rate for U.S. based non-exempt (hourly) employees)
# Bonus Target Percentage = see chart above

# Your bonus target will be calculated using your annual base salary in effect April 1, 2023 (your annual salary resulting from the annual salary planning cycle).

# For New Hires after January 1, 2023
# If you start your Yahoo employment after January 1, 2023, your bonus target will be prorated accordingly. For example, if you were hired on June 1, 2023, your eligibility would be based on 214 days out of 365 days. If your first day of Yahoo employment occurs after September 30, 2023, you will not be eligible for a 2023 bonus.

# For employees promoted after January 1, 2023:
# If your target bonus changes during the bonus plan year, your bonus target will be prorated accordingly. For example, if you are promoted from IC2 to IC3 on June 1, 2023, your target bonus would be based on your base salary and IC2 target bonus for 151 days (annual salary in effect April 1, 2023 x 10% x 151/365) and your base salary and IC3 target bonus for 214 days (annual salary in effect June 1, 2023 x 15% x 214/365).

# For employees who have a change in base salary (if promoted effective January 1, 2023 and receive a salary increase thereafter; if you received a salary increase after 2023 annual salary planning cycle (April 1, 2023)):
# If your base salary changes during the bonus plan year, your bonus target will be prorated for the time spent at the different salary rates. For example, if you received a salary increase effective June 1, 2023, your target bonus would be based on your prior base salary in effect April 1, 2023 for 151 days and your new base salary for the remaining 214 days.'''
# query = "New Hires after January 1, 2023"
# window_size = 1000
# delimiters = ["<END>"]
# result = find_text_window(query, context, window_size, delimiters)
# print(result)
# print(len(result))

    window_size = window_size - len(query)
    query_index = context_text.find(query)
    if query_index == -1:
        return "Query not found in the context."

    # Calculate half window size for left and right of the query
    half_window = window_size // 2

    # Initialize window start and end positions
    start = max(0, query_index - half_window)
    end = min(len(context_text), query_index + len(query) + half_window)

    # Adjust for delimiters on the left side
    left_context = context_text[:query_index]
    for delim in delimiters:
        delim_index = left_context.rfind(delim, max(0, query_index - window_size), query_index)
        if delim_index != -1:
            start = delim_index + len(delim)
            break

    # Adjust for delimiters on the right side
    right_context = context_text[query_index + len(query):]
    for delim in delimiters:
        delim_index = right_context.find(delim, 0, min(len(right_context), half_window))
        if delim_index != -1:
            end = query_index + len(query) + delim_index
            break

    return context_text[start:end]