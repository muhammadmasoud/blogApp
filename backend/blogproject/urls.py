from django.contrib import admin

from django.urls import path,include
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('blog.urls')),
    path('api/', include('blog.urls')),
    
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
