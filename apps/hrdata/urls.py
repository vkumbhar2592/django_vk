from django.urls import path
from .views import LoadTextFilesIntoSQL, TopicListView, TopicDetailView, TopicCreateView, TopicUpdateView, TopicDeleteView, TagListView, TagDetailView, TagCreateView, TagUpdateView, TagDeleteView, DocumentListView, DocumentDetailView, DocumentCreateView, DocumentUpdateView, DocumentDeleteView, RegionListView, RegionDetailView, RegionCreateView, RegionUpdateView, RegionDeleteView
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from .views import SaveDocumentsIntoFaiss
from .views import FaissChunksView

def is_authenticated(user):
    return user.is_authenticated

urlpatterns = [
    path('topic/', user_passes_test(is_authenticated, login_url='/admin/login/')(TopicListView.as_view()), name='topic_list'),
    path('topic/<int:pk>/', user_passes_test(is_authenticated, login_url='/admin/login/')(TopicDetailView.as_view()), name='topic_detail'),
    path('topic/create/', user_passes_test(is_authenticated, login_url='/admin/login/')(TopicCreateView.as_view()), name='topic_create'),
    path('topic/<int:pk>/update/', user_passes_test(is_authenticated, login_url='/admin/login/')(TopicUpdateView.as_view()), name='topic_update'),
    path('topic/<int:pk>/delete/', user_passes_test(is_authenticated, login_url='/admin/login/')(TopicDeleteView.as_view()), name='topic_delete'),
    path('tag/', user_passes_test(is_authenticated, login_url='/admin/login/')(TagListView.as_view()), name='tag_list'),
    path('tag/<int:pk>/', user_passes_test(is_authenticated, login_url='/admin/login/')(TagDetailView.as_view()), name='tag_detail'),
    path('tag/create/', user_passes_test(is_authenticated, login_url='/admin/login/')(TagCreateView.as_view()), name='tag_create'),
    path('tag/<int:pk>/update/', user_passes_test(is_authenticated, login_url='/admin/login/')(TagUpdateView.as_view()), name='tag_update'),
    path('tag/<int:pk>/delete/', user_passes_test(is_authenticated, login_url='/admin/login/')(TagDeleteView.as_view()), name='tag_delete'),
    path('region/', user_passes_test(is_authenticated, login_url='/admin/login/')(RegionListView.as_view()), name='region_list'),
    path('region/<int:pk>/', user_passes_test(is_authenticated, login_url='/admin/login/')(RegionDetailView.as_view()), name='region_detail'),
    path('region/create/', user_passes_test(is_authenticated, login_url='/admin/login/')(RegionCreateView.as_view()), name='region_create'),
    path('region/<int:pk>/update/', user_passes_test(is_authenticated, login_url='/admin/login/')(RegionUpdateView.as_view()), name='region_update'),
    path('region/<int:pk>/delete/', user_passes_test(is_authenticated, login_url='/admin/login/')(RegionDeleteView.as_view()), name='region_delete'),
    path('document/', user_passes_test(is_authenticated, login_url='/admin/login/')(DocumentListView.as_view()), name='document_list'),
    path('document/<int:pk>/', user_passes_test(is_authenticated, login_url='/admin/login/')(DocumentDetailView.as_view()), name='document_detail'),
    path('document/create/', user_passes_test(is_authenticated, login_url='/admin/login/')(DocumentCreateView.as_view()), name='document_create'),
    path('document/<int:pk>/update/', user_passes_test(is_authenticated, login_url='/admin/login/')(DocumentUpdateView.as_view()), name='document_update'),
    path('document/<int:pk>/delete/', user_passes_test(is_authenticated, login_url='/admin/login/')(DocumentDeleteView.as_view()), name='document_delete'),
    path('reindex-documents/', user_passes_test(is_authenticated, login_url='/admin/login/')(SaveDocumentsIntoFaiss.as_view()), name='reindex-documents'),
    path('faiss-chunks/', user_passes_test(is_authenticated, login_url='/admin/login/')(FaissChunksView.as_view()), name='faiss_chunks'),
    path('LoadTextFilesIntoSQL/', user_passes_test(is_authenticated, login_url='/admin/login/')(LoadTextFilesIntoSQL.as_view()), name='LoadTextFilesIntoSQL'),


]
