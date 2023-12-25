from django.urls import path
from .views import TableView
from django.contrib.auth.decorators import user_passes_test
from .views import document_update_view  # Import your view function

def is_authenticated(user):
    return user.is_authenticated

 

urlpatterns = [
    path(
        "view/",
        user_passes_test(is_authenticated, login_url='/admin/login/')(TableView.as_view(template_name="dash.html")),
        name="tables-datatables-extensions",
    ),
    path(
        "docs/",
        user_passes_test(is_authenticated, login_url='/admin/login/')(TableView.as_view(template_name="docs.html")),
        name="docs",
    ),
    path(
        "docs/<int:pk>",
        user_passes_test(is_authenticated, login_url='/admin/login/')(TableView.as_view(template_name="doc.html")),
        name="docs",
    ),
    path(
        "docs/update/<int:pk>/",  # URL pattern for updating a document
        user_passes_test(is_authenticated, login_url='/admin/login/')(document_update_view),
        name="document_update_url",  # Unique name for the update view
    ),
]
