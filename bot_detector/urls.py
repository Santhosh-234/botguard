from django.contrib import admin
from django.urls import path, re_path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from api.views import analyze_twitter_user

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/analyze/', analyze_twitter_user, name='analyze_twitter_user'),
    # Serve React App
    re_path(r'^.*', TemplateView.as_view(template_name='index.html')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 