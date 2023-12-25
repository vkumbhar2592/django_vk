from django.urls import path
from .views import ChatView
from . import views
from django.contrib.auth.decorators import user_passes_test


def is_authenticated(user):
    if user.is_authenticated:
        return  user.email.endswith('@gmail') or user.email.startswith('local')
    return False


urlpatterns = [
    path("logout/", views.logout_view, name="logout"),
    # path('api/answer/', views.answer, name='answer'),
    path('api/answer_stream/', views.answer_stream, name='stream-response'), 
    path('api/update_like/', views.update_like_status, name='update_like'),
    path('api/update_dislike/', views.update_dislike_status, name='update_dislike_status'),
    path('api/update_dislike_comment/', views.update_dislike_comment, name='update_dislike_comment'),
    path('api/update_bookmark/', views.update_bookmark, name='update_bookmark'),
    path(
        "",
        user_passes_test(is_authenticated, login_url='/accounts/google/login/?next=/')(ChatView.as_view(template_name="chat.html")),
        name="tables-datatables-extensions",
    ), 

]
