import datetime
from django.views.generic import TemplateView
from . import TemplateLayout
from django.shortcuts import render
from langchain.embeddings import HuggingFaceBgeEmbeddings
from langchain.vectorstores import FAISS
from django.shortcuts import get_object_or_404

from django.http import StreamingHttpResponse 
import requests
import json
import sseclient
import os

from llama_index.agent import OpenAIAgent
from llama_index.llms import OpenAI
from llama_index.llms import OpenAI, ChatMessage
from llama_index.tools import BaseTool, FunctionTool
import json
from typing import Sequence, List

from django.http import JsonResponse

from django.contrib.auth import logout
from django.conf import settings
from openai import OpenAI

import datetime
from .models import ChatLog
from django.contrib.auth.decorators import login_required
from apps.hrdata.utils import get_full_docs_after_faiss

# GPT_MODEL_4 = "gpt-4-1106-preview"
GPT_MODEL_4 = "gpt-4-32k"
GPT_MODEL_3 = "gpt-3.5-turbo-1106"
MODEL_NAME = GPT_MODEL_4

TEMP=0
MAX_TOKENS=2000
TOP_P=0.1
FREQUENCY_PENALTY=0.5
PRESENSE_PENALTY=0.5


import nest_asyncio

def multiply(a: int, b: int) -> int:
    """Multiple two integers and returns the result integer"""
    return a * b

def add(a: int, b: int) -> int:
    """Add two integers and returns the result integer"""
    return a + b


add_tool = FunctionTool.from_defaults(fn=add)
nest_asyncio.apply()
multiply_tool = FunctionTool.from_defaults(fn=multiply)

# llm = OpenAI(model= GPT_MODEL_4)
# agent = OpenAIAgent.from_tools(
#     [multiply_tool, add_tool], llm=llm, verbose=True
# )


"""
This file is a view controller for multiple pages as a module.
Here you can override the page view layout.
Refer to sample/urls.py file for more pages.
"""


def logout_view(request):
    logout(request)
    data = {"message": "logged out!"}
    return JsonResponse(data)
    # return render(request, "/")

class ChatView(TemplateView): 
    def get_context_data(self, **kwargs): 
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        return context


def answer_stream(request): 
    long_query = request.GET.get('q', '') 
    
    
    # Call the get_full_docs_after_faiss function
    result = get_full_docs_after_faiss(long_query) 
    
    sources = [r.street_url for r in result]
    source_names = [r.name for r in result]
    content_list = [r.content for r in result]
    context_str = '\n\n'.join([f"CONTEXT name: '{source_names[i]}' | CONTEXT  URL: '{sources[i]}'  :\n\n CONTEXT Data :\n {content}\n\n" for i, content in enumerate(content_list)]) 
    prompt = preparePrompt(context_str, long_query)  
    
    # Create a new ChatLog instance
    chat_log = ChatLog(
        question=long_query,
        prompt=prompt,  # Assuming you have the prompt variable prepared as before
        # Initialize other fields as necessary
    )
    # Save the initial state of the ChatLog
    chat_log.save() 

    return StreamingHttpResponse(streamOpenAI(prompt, chat_log, result), content_type="text/event-stream")


 
def update_like_status(request):
    chatlog_id = request.GET.get('chatlog_id')
    comment = request.GET.get('comment')
    if chatlog_id:
        chatlog = get_object_or_404(ChatLog, id=chatlog_id)
        chatlog.is_liked = True
        chatlog.is_disliked = False
        chatlog.comment = comment or ''
        chatlog.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'ChatLog ID not provided'}, status=400)

def update_dislike_status(request):
    chatlog_id = request.GET.get('chatlog_id')
    comment = request.GET.get('comment')
    if chatlog_id:
        chatlog = get_object_or_404(ChatLog, id=chatlog_id)
        chatlog.is_disliked = True
        chatlog.is_liked = False
        chatlog.comment = comment or ''
        chatlog.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'ChatLog ID not provided'}, status=400)



def update_dislike_comment(request):
    chatlog_id = request.GET.get('chatlog_id')
    comment = request.GET.get('comment') 
    
    if chatlog_id:
        chatlog = get_object_or_404(ChatLog, id=chatlog_id) 
        if comment:
            chatlog.comment = comment
        chatlog.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'ChatLog ID not provided'}, status=400)


def update_bookmark(request):
    chatlog_id = request.GET.get('chatlog_id')
    bookmark = request.GET.get('bookmark') 
    if chatlog_id:
        chatlog = get_object_or_404(ChatLog, id=chatlog_id)
        if bookmark: 
            is_bookmarked = bookmark == '1' 
            chatlog.is_bookmarked = is_bookmarked
        chatlog.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'ChatLog ID not provided'}, status=400)


def get_parents(result):
    parents_list = set()
    print(len(result)) 
    for r in result:
        try:
            doc_id =  r.metadata['doc_id']
            # print(">>>>>>>>>>>>> " +  doc_id)
            parents_list.add(doc_id)
        except :
            pass 
    return parents_list

def preparePrompt( documents, q):
    today = datetime.date.today()
    current_month = datetime.datetime.now().month
    now = datetime.datetime.now()
     
 
    prompt = f'''
        Question:
        {q}

        --------------------
        Today is  {str(today)}  . The time is  {str(now.hour)}:{str(now.minute)}:{str(now.second)} .
        --------------------
        
        
        CONTEXT:

        {documents}
        --------------------

        Task:
        Please reformulate and expand my question for clarity, but provide your answer based on the original question without including the reformulated versions
        If the user is casually chatting with you, you can respond with a casual answer and include a dad joke about technology or internet or AI.
        If the user is asking a question, you should provide a clear and concise answer and do not include any dad jokes.


        Go over the different contexts and make sure you understand them well. Then ignore the ones that are not relevant to the question.
        Do not include your logic in the answer. Only include the answer itself.


        If the question doesn't mention which Yahoo office, use the US Yahoo office as the default.
        If the question is related to HR and just mentions a region, use that Yahoo office as default.


        IMPORTANT: Please use lists and put each element in a div when appropriate for better readability.

        Answer as a nice and friendly HR assistant and  USE LANGUAGE FROM THE CONTEXT AS MUCH AS POSSIBLE.
        MAKE SURE YOUR ANSWER IS CORRECT and relevant.


        Please provide the answer with clearly separated sections for each part of the response.
        Use 'div' elements to encapsulate each block of text, and include 'h6' tags for the headings of each section, rather than 'h2'.
        The goal is to have a neatly organized output that is easy to read and well-structured.
        Make sure the answer is comprehensive.


        Boldest the important words in the answer.

        Please provide an answer to my question with detailed information. For each section in your response,
        include a hyperlink that points to the specific source or reference you used for that information.
        Format the hyperlink as follows:  <a href='URL' target="_blank">URL_Title</a> . The URL title should be CONTEXT NAME provided in the CONTEXT.
        This will help in identifying which parts of the answer are based on which sources.
        if the link has the form of yo/LINK , just add http to it looks like http://yo/LINK

answer:

        
        ''' 
    # Based on the question and the provided context, append your response with a follow up question that's answer already exists in the context.

    #     Have the follow up question in a div with the following format:
    #     <div class='follow-up-question'>FOLLOW_UP_QUESTION</div>
    # print(f"Prompt: {prompt}")
    return prompt

def callOpenAI( prompt):
    client = OpenAI()

    response = client.chat.completions.create(
        model=GPT_MODEL_3,
        messages=[
            {
            "role": "system",
            "content": system_prompt
            },
            {
            "role": "user",
            "content": prompt
            }
        ],
        temperature=TEMP,
        max_tokens=MAX_TOKENS,
        top_p=TOP_P,
        frequency_penalty=FREQUENCY_PENALTY,
        presence_penalty=PRESENSE_PENALTY
    ) 
    return  {'response': response.choices[0].message.content }

 
def streamOpenAI(prompt,  chat_log, documents): 
    response_content = ""
    sent_chat_log_id = False  # Flag to track if ChatLog ID has been sent
    sent_source_url = False  # Flag to track if ChatLog ID has been sent

    def event_stream(): 
        nonlocal response_content, sent_chat_log_id, sent_source_url
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"
        }
        data = {
            "model":MODEL_NAME,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt }
            ],
            "temperature": TEMP,
            "stream": True, 
            'max_tokens': MAX_TOKENS,
            'top_p': TOP_P,
            'frequency_penalty' : FREQUENCY_PENALTY,
            'presence_penalty' : PRESENSE_PENALTY
        } 


        with requests.post(url, headers=headers, data=json.dumps(data), stream=True) as response:
            if response.status_code != 200:
                print(f"Error: {response.status_code}, {response.text}")
                return
            for line in response.iter_lines():
                # print(line)
                if line:
                    
                    line_str = line.decode('utf-8').replace('data: ', '')
                    if line_str == '[DONE]':
                        print('Stream ended.')
                        break  # Exit the loop when end of stream is reached

                    try:
                        json_data = json.loads(line_str)
                        if 'choices' in json_data and json_data['choices']:
                            for choice in json_data['choices']:
                                if 'delta' in choice and 'content' in choice['delta']:
                                    content = choice['delta']['content']

                                    # Check if ChatLog ID needs to be sent
                                    if not sent_chat_log_id:
                                        yield f"data: {json.dumps({'chat_log_id': chat_log.id})}\n\n"
                                        sent_chat_log_id = True
                                    # Check if ChatLog ID needs to be sent
                                    if not sent_source_url:
                                        sources = [r.name +'|' + r.street_url for r in documents]
                                        yield f"data: {json.dumps({'source': sources})}\n\n"
                                        sent_source_url = True
                                    
                                    # Then yield the actual content
                                    yield f"data: {json.dumps({'content': content})}\n\n"
                                    response_content += content
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON: {e}")
                        
        if response_content:
            # After receiving the complete response, update the ChatLog instance
            chat_log.response = response_content   
            chat_log.model_name = MODEL_NAME   
            chat_log.prompt = prompt   
            chat_log.save()

    return StreamingHttpResponse(event_stream(), content_type='text/event-stream')


system_prompt = '''
    You are a highly consistent and reliable Yahoo HR assistant agent designed to help Yahoo employees get answers to their questions. You can answer questions related to PTO, Career Development, Learning, PTO, etc... Your responses should be concise, comprehensive, and use simple language. 

    Remember the following guidelines:
    1. All the context provided is from Yahoo HR.
    2. Every mention of Yahoo refers to Yahoo Inc or Yahoo Office.
    3. Provide consistent answers. For the same query, always give the same response.
    4. Avoid making assumptions or "hallucinations" that are not grounded in the provided HR documentation.
    5. If the answer is not found in the provided document, clearly state that you do not know the answer.
    
    \n\n
'''