from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
import shutil 

from .utils import RecursiveCharacterTextSplitter, get_faiss_chunks, get_full_docs_after_faiss
# Create your views here.

from .models import Topic, Tag, Document, Region
from .serializers import TopicSerializer, TagSerializer, DocumentSerializer, RegionSerializer
from rest_framework.views import APIView
from langchain.embeddings import HuggingFaceBgeEmbeddings 
from langchain.vectorstores import FAISS

# model_name = "BAAI/bge-small-en"
# encode_kwargs = {'normalize_embeddings': True}
# embeddings = HuggingFaceBgeEmbeddings(model_name=model_name, encode_kwargs=encode_kwargs)
# persist_directory = "../faiss_index"
# faiss_index = FaissIndex(embedding_size=embeddings.embedding_size, persist_directory=persist_directory)



from transformers import AutoTokenizer, AutoModel
import numpy as np
import torch
from langchain.schema import Document as LCDocument
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.embeddings import OpenAIEmbeddings
from langchain.embeddings import CohereEmbeddings
from langchain.vectorstores.faiss import FAISS
from django.conf import settings
from pathlib import Path
import os
from django.http import JsonResponse
from django.views import View 


embeddings = OpenAIEmbeddings()


class LoadTextFilesIntoSQL(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser] 
    
    def get(self, request, format=None):
        # Delete all existing documents
        Document.objects.all().delete()
        print("All existing documents have been deleted.")
        directory = Path(__file__).resolve().parent / 'initial_data_clean'
        for filename in os.listdir(directory):
            if filename.endswith(".txt"):
                file_path = os.path.join(directory, filename)

                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()

                    # Extract parts of the file
                    source = extract_line_after(content, 'Source:')
                    title = extract_line_after(content, 'Title:')
                    document_content = content.split('Document:', 1)[1] if 'Document:' in content else content

                    # Create and save the Document object
                    Document.objects.create(name=title, street_url=source, content=document_content, topic_id=1, region_id=1)
                    print(f"Document {title} saved successfully.")
        return Response({"message": "Documents loaded successfully."})

def extract_line_after(text, keyword):
        try:
            return text.split(keyword, 1)[1].split('\n', 1)[0].strip()
        except IndexError:
            return ''
 
class SaveDocumentsIntoFaiss(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser] 
    
    # embeddings = CohereEmbeddings(cohere_api_key= settings.COHERE_API_KEY)
    def get(self, request, format=None): 

        list_of_documents = []
        documents = Document.objects.all()
        for document in documents:
            splitter = RecursiveCharacterTextSplitter(chunk_size=settings.CHUNK_SIZE , separators=settings.CHUNCK_SEPARATOR)
            docs = splitter.split(document.content)
            for doc in docs:
                # print(doc)
                # print('--')
                list_of_documents.append(LCDocument(page_content=doc, metadata=dict(id=document.id)))  # FAISS expects numpy array
        try:
            folder_path = settings.FAISS_DB

            # Check if the folder exists
            if os.path.exists(folder_path) and os.path.isdir(folder_path):
                shutil.rmtree(folder_path)
                print(f"Folder '{folder_path}' has been removed")
            else:
                print(f"Folder '{folder_path}' does not exist")
        except:
            # Add documents to the FAISS index
            print("Error while removing folder")
        db = FAISS.from_documents(list_of_documents, embeddings)
        db.save_local(settings.FAISS_DB)
        return Response({"message": "Documents reindexed successfully."})
        

class FaissChunksView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    # serializer_class = DocumentSerializer
    
    def get(self, request, format=None):
        result = []
        query = self.request.query_params.get('query', None)
        result = get_full_docs_after_faiss(query)
        return Response({"result": result}) 
    

class TopicListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

    def get_queryset(self):
        queryset = Topic.objects.all()
        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name__icontains=name)
        return queryset
    
class TopicDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

class TopicCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

class TopicUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

class TopicDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

class TagListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def get_queryset(self):
        queryset = Tag.objects.all()
        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name__icontains=name)
        return queryset
    
class TagDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class TagCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class TagUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class TagDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Tag.objects.all()
    serializer_class = TagSerializer



class RegionListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Region.objects.all()
    serializer_class = RegionSerializer

    def get_queryset(self):
        queryset = Region.objects.all()
        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name__icontains=name)
        return queryset

class RegionDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Region.objects.all()
    serializer_class = RegionSerializer

class RegionCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Region.objects.all()
    serializer_class = RegionSerializer

class RegionUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Region.objects.all()
    serializer_class = RegionSerializer

class RegionDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Region.objects.all()
    serializer_class = RegionSerializer



class DocumentListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    def get_queryset(self):
        queryset = Document.objects.all()
        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name__icontains=name)
        return queryset
 
    

class DocumentDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

class DocumentCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

class DocumentUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

class DocumentDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
 
