from django.conf import settings
import getpass
import os
from langchain.document_loaders import DirectoryLoader 
from langchain.embeddings import HuggingFaceBgeEmbeddings
from langchain.text_splitter import CharacterTextSplitter,RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.vectorstores.faiss import DistanceStrategy

# Define model and encoding parameters
model_name = "BAAI/bge-small-en" 

    # EUCLIDEAN_DISTANCE = "EUCLIDEAN_DISTANCE"
    # MAX_INNER_PRODUCT = "MAX_INNER_PRODUCT"
    # DOT_PRODUCT = "DOT_PRODUCT"
    # JACCARD = "JACCARD"
    # COSINE = "COSINE"

encode_kwargs = {'normalize_embeddings': True} # set True to compute cosine similarity

# Initialize embeddings function
embeddings = HuggingFaceBgeEmbeddings(
    model_name=model_name,
    encode_kwargs=encode_kwargs
)

db = FAISS.load_local("../../DBs/faiss_index_2", embeddings)
    

long_query = "How is my bonus target amount calculated?"
docs = db.similarity_search_with_score(long_query, k=8 ,distance_strategy='COSINE')

# print(len(docs))
 
# for doc, score in docs:
#     print("#"*100)
#     print(f"Content: {doc.page_content}, Metadata: {doc.metadata}, Score: {score}")

def find_text_window(query, context_text, window_size, delimiters):
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


# Example usage
context = '''
BONUS PLAN MECHANICS

Q: Which job levels qualify for this plan and what are the bonus targets for each?
A: The bonus target is a percentage of the base salary for each eligible level as follows:

In the job category of E1, the title is "VP" and has a bonus target of 35%. For M6 / IC7, the title is "Senior Director" with a bonus target of 30%. M5 / IC6 corresponds to the title "Director" and carries a bonus target of 25%. The title "Senior Manager" is associated with M4 / IC5 and has a bonus target of 15%. Both M3 / IC4, with the title "Manager", and M2 / IC3, with the title "Assoc Manager / Career Professional", have a bonus target of 15%. IC2 is designated as "Developing Professional" with a bonus target of 10%. IC1, referred to as "Entry Professional", has a bonus target of 5%. Lastly, the categories S1 through S4 are collectively labeled as "Support" and each have a bonus target of 5%.

*SVP and above targets are undisclosed.
Refer here for your job level.

Q: How is my bonus target amount calculated?
A: Annual Base Salary x Bonus Target Percentage: ($100 x 10% = $10)
Annual Salary = Annual Base Pay (based on regular hourly rate for U.S. based non-exempt (hourly) employees)
Bonus Target Percentage = see chart above

Your bonus target will be calculated using your annual base salary in effect April 1, 2023 (your annual salary resulting from the annual salary planning cycle).

For New Hires after January 1, 2023
If you start your Yahoo employment after January 1, 2023, your bonus target will be prorated accordingly. For example, if you were hired on June 1, 2023, your eligibility would be based on 214 days out of 365 days. If your first day of Yahoo employment occurs after September 30, 2023, you will not be eligible for a 2023 bonus.

For employees promoted after January 1, 2023:
If your target bonus changes during the bonus plan year, your bonus target will be prorated accordingly. For example, if you are promoted from IC2 to IC3 on June 1, 2023, your target bonus would be based on your base salary and IC2 target bonus for 151 days (annual salary in effect April 1, 2023 x 10% x 151/365) and your base salary and IC3 target bonus for 214 days (annual salary in effect June 1, 2023 x 15% x 214/365).

For employees who have a change in base salary (if promoted effective January 1, 2023 and receive a salary increase thereafter; if you received a salary increase after 2023 annual salary planning cycle (April 1, 2023)):
If your base salary changes during the bonus plan year, your bonus target will be prorated for the time spent at the different salary rates. For example, if you received a salary increase effective June 1, 2023, your target bonus would be based on your prior base salary in effect April 1, 2023 for 151 days and your new base salary for the remaining 214 days.'''
query = "New Hires after January 1, 2023"
window_size = 1000
delimiters = ["<END>"]
result = find_text_window(query, context, window_size, delimiters)
print(result)
print(len(result))