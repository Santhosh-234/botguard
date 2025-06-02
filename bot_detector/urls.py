from django.contrib import admin
from django.urls import path
from api.views import TwitterUserView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/analyze/', TwitterUserView.as_view(), name='analyze-user'),
] 