
from django.contrib import admin
from django.urls import include, path
from web_project.views import SystemView

urlpatterns = [
    path("admin/", admin.site.urls),

    path("accounts/", include("allauth.urls")),
    # starter urls
    path("", include("apps.sample.urls")),
    path("manage/", include("apps.hrdata.urls")),
    path("dash/", include("apps.tables.urls")),
    path("chat/", include("apps.chat.urls")),
]

handler404 = SystemView.as_view(template_name="pages/system/not-found.html", status=404)
handler500 = SystemView.as_view(template_name="pages/system/error.html", status=500)



