
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('dressup/', include('dressup.urls', 'dressup'), name='dressup'),
    path('journal/', include(('journal.urls', 'journal'), namespace='journal')),
    path('', RedirectView.as_view(url='/journal/', permanent=False)),  # Redirect root URL to journal
    # Add other URL patterns here
    re_path(r'^.*', RedirectView.as_view(url='/journal/', permanent=False)),  # Redirect all other URLs to journal
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
